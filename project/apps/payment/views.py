from django.shortcuts import render, redirect
from apps.product.models import BasketItem
from .delivery.wolt import Delivery
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .epoint.payment import Payment
from rest_framework.generics import CreateAPIView
from .serializer import TransactionSerializer
from .models import Transaction
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse
from apps.product.models import Product, Coupon, Order, OrderItem, CouponUsage
from apps.product.views import apply_coupon
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from utils.time_helper.is_active_time import is_active_time

from django.contrib.auth import get_user_model

User = get_user_model()
def payment(request):
    # payment_obj = Payment()
    # payment_obj.checkout_request()
    return render(request, 'payment.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from urllib.parse import urlparse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class SuccessView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        transaction_obj = self.get_last_transaction(user)

        if not transaction_obj:
            messages.error(request, "No transaction found.")
            return redirect('basket')

        payment_obj = Payment()
        response_data = payment_obj.get_payment_status(transaction_obj)

        if response_data["status"] == 'success' and not transaction_obj.is_checked_from_eco:
            return self.handle_successful_payment(request, user, transaction_obj)
        elif response_data["status"] == 'new':
            return self.handle_new_payment(transaction_obj)

        return redirect('failed')

    def get_last_transaction(self, user):
        """Fetch the last transaction for the user."""
        return Transaction.objects.filter(user=user).last()

    @transaction.atomic
    def handle_successful_payment(self, request, user, transaction_obj):
        try:
            basket_items = BasketItem.objects.filter(user=user)

            if not basket_items.exists():
                return redirect('basket')

            # Stock check
            if not self.check_stock(request, basket_items):
                return redirect('basket')

            # Calculate total amount
            total_amount = sum(item.total_price for item in basket_items)

            # Handle coupon
            applied_coupon = self.get_valid_coupon(transaction_obj.coupon_code, user)
            if transaction_obj.coupon_code and not applied_coupon:
                return redirect('basket')

            # Calculate the discount and final total amount
            discount_amount = self.apply_coupon(user, basket_items, applied_coupon) if applied_coupon else 0
            is_delivery_free = (applied_coupon and discount_amount > 30) or (total_amount > 30)

            # Ensure delivery_amount is not None
            delivery_amount = transaction_obj.delivery_amount or 0

            discount = total_amount - discount_amount
            total_amount += delivery_amount if not is_delivery_free else 0

            # Create order
            order = self.create_order(user, transaction_obj, total_amount, discount_amount, discount,  applied_coupon, is_delivery_free)

            # Update stock and order items
            self.update_stock_and_order_items(order, basket_items)

            # Clear the basket
            basket_items.delete()

            # Update coupon usage if applied
            if applied_coupon:
                self.update_coupon_usage(applied_coupon, user)

            # Handle Wolt delivery if applicable
            if transaction_obj.is_wolt:
                if not self.handle_wolt_delivery(order):
                    return redirect('basket')

            transaction_obj.is_checked_from_eco = True
            transaction_obj.save()

            return render(request, 'success.html')

        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while creating the order.')
            return redirect('basket')

    
    def handle_new_payment(self, transaction_obj):
        """Handle a payment with a 'new' status."""
        return render(self.request, 'failed.html', context={"payment_redirect_url": transaction_obj.payment_redirect_url})

    def check_stock(self, request, basket_items):
        """Check if all items are in stock."""
        for item in basket_items:
            product = Product.objects.get(id=item.product.id)
            if item.quantity > product.stock:
                messages.error(request, f"'{product.title}' is out of stock.")
                return False
        return True

    def get_valid_coupon(self, coupon_code, user):
        """Validate the coupon code."""
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon=coupon_code)
                if coupon.can_user_use_coupon(user):
                    return coupon
            except Coupon.DoesNotExist:
                return None
        return None

    def apply_coupon(self, user, basket_items, applied_coupon):
        """Calculate the discount based on the coupon."""
        if applied_coupon:
            # Assuming apply_coupon is a utility function that calculates the discount
            return apply_coupon(user, basket_items, applied_coupon)
        return 0

    def create_order(self, user, transaction_obj, total_amount, discount_amount, discount,  applied_coupon, is_delivery_free):
        """Create the order based on the transaction and basket items."""
        return Order.objects.create(
            user=user,
            total_amount=total_amount,
            discount=discount if applied_coupon else None,
            discount_amount=discount_amount,
            delivery_amount=transaction_obj.delivery_amount,
            is_delivery_free=is_delivery_free,
            coupon=applied_coupon,
            is_wolt=transaction_obj.is_wolt,
            transaction=transaction_obj
        )

    def update_stock_and_order_items(self, order, basket_items):
        """Update the stock and add items to the order."""
        for item in basket_items:
            product = Product.objects.get(id=item.product.id)
            order_item = OrderItem.objects.create(order=order, product=product, quantity=item.quantity)
            print(order_item)
            # Decrease stock
            product.stock -= item.quantity
            product.sale_count += item.quantity
            product.save()

    def update_coupon_usage(self, coupon, user):
        """Update the usage count for the coupon."""
        coupon_usage = CouponUsage.objects.get(user=user, coupon=coupon)
        coupon_usage.max_coupon_usage_count -= 1
        coupon_usage.save()

    def handle_wolt_delivery(self, order):
        """Handle the Wolt delivery process."""
        user_order_items = OrderItem.objects.filter(order=order).order_by("pk")
        parcel_list = [item.to_dict_for_wolt_delivery() for item in user_order_items]
        
        delivery = Delivery(lat=order.transaction.lat, lon=order.transaction.lon)
        delivery_response = delivery.deliveries(
            amount=order.transaction.delivery_amount,
            recipient_name=order.transaction.recipient_name,
            recipient_phone=order.transaction.recipient_phone,
            dropoff_comment=order.transaction.dropoff_comment,
            parcel_list=parcel_list,
            shipment_promise_id=order.transaction.shipment_promise_id
        )

        if "error_code" in delivery_response:
            # Handle error scenario
            messages.error(self.request, 'An error occurred with the delivery service.')
            return False

        if 'tracking' in delivery_response:
            tracking_url = delivery_response["tracking"]["url"]
            tracking_id = delivery_response["tracking"]["id"]
            wolt_order_reference_id = delivery_response["wolt_order_reference_id"]
            
            if not all([tracking_url, tracking_id, wolt_order_reference_id]):
                messages.error(self.request, 'Invalid delivery response.')
                return False

            parsed_url = urlparse(tracking_url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                messages.error(self.request, 'Invalid tracking URL.')
                return False

            # Save the extracted data to the Order instance
            order.tracking_url = tracking_url
            order.tracking_id = tracking_id
            order.wolt_order_reference_id = wolt_order_reference_id
            order.save()

        return True


def failed(request):
    # transaction_obj = Transaction.objects.filter(user = request.user, ).last()
    return render(request, 'failed.html')

def result(request):
    return render(request, 'result.html')

def map(request):
    if not is_active_time():
        return redirect("home")
    # payment_obj = Payment()
    # payment_obj.checkout_request()
    context = {
        "items": BasketItem.objects.filter(user = request.user).order_by("pk")
    }
    if(context['items'].count() > 0):
        return render(request, 'delivery.html', context = context)
    else:
        return redirect("home")

def shipment_promises(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    street = request.GET.get('street')
    if lat and lon:
        delivery = Delivery(lat = lat, lon = lon, street = street)
        return JsonResponse(delivery.shipment_promises())
    return JsonResponse({"message": "Please send lat and lon value"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_request_api_view(request):
    amount = request.data.get('amount')
    language = request.data.get('language')
    if not amount:
        return Response('Amount is missing')
    # if not language:
    #     return Response('Language is missing')
    payment_obj = Payment()
    response = payment_obj.checkout_request(amount = amount, language = language)
    return Response(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deliveries(request):
    lat = request.data.get('lat')
    lon = request.data.get('lon')
    amount = request.data.get('amount')
    recipient_name = request.data.get('recipient_name')
    recipient_phone = request.data.get('recipient_phone')
    dropoff_comment = request.data.get('dropoff_comment')
    shipment_promise_id = request.data.get('shipment_promise_id')
    user_basket_items = BasketItem.objects.filter(user=request.user).order_by("pk")
    parcel_list = [item.to_dict_for_wolt_delivery() for item in user_basket_items]
    if lat and lon and amount and recipient_name and recipient_phone and dropoff_comment and parcel_list and shipment_promise_id:
        delivery = Delivery(lat = lat, lon = lon)
        return Response(delivery.deliveries(amount = amount, recipient_name = recipient_name, recipient_phone = recipient_phone, dropoff_comment = dropoff_comment, parcel_list = parcel_list, shipment_promise_id = shipment_promise_id))
    return Response({"message": "Please enter correct datas."})

class TransactionCreateAPIView(CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        # POST isteği ile gelen verileri al
        incoming_data = serializer.validated_data

        # Gelen verileri logla veya başka bir işlem yap
        print(incoming_data)

        # Veriyi kaydet
        serializer.save(user=self.request.user)