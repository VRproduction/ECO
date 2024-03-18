from django.shortcuts import render, redirect
from product.models import BasketItem
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
from product.models import Product, Coupon, Order, OrderItem, CouponUsage
from product.views import apply_coupon
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction

def payment(request):
    # payment_obj = Payment()
    # payment_obj.checkout_request()
    return render(request, 'payment.html')

@transaction.atomic
@login_required
def success(request):
    context = {

    }
    transaction_obj = Transaction.objects.filter(user = request.user).last()
    payment_obj = Payment()
    response_data = payment_obj.get_payment_status(transaction_obj)  
    print(response_data)  
    if response_data["status"] == 'success' and not transaction_obj.is_checked_from_eco:
        if transaction_obj.is_wolt:
            user_basket_items = BasketItem.objects.filter(user=request.user).order_by("pk")
            parcel_list = [item.to_dict_for_wolt_delivery() for item in user_basket_items]
            delivery = Delivery(lat = transaction_obj.lat, lon = transaction_obj.lon)
            delivery_response = delivery.deliveries(amount = transaction_obj.amount, recipient_name = transaction_obj.recipient_name, recipient_phone = transaction_obj.recipient_phone, parcel_list = parcel_list, shipment_promise_id = transaction_obj.shipment_promise_id)
            print(delivery_response)
            if "error_code" in delivery_response:
                print(delivery_response["error_code"])
                # pul qaytarilmali olan funksiya
                return redirect('failed')
            elif 'tracking' in delivery_response:
                tracking_url = delivery_response["tracking"]["url"]
                tracking_id = delivery_response["tracking"]["id"]
                wolt_order_reference_id = delivery_response["wolt_order_reference_id"]
                    
                errors = []

                if not tracking_url:
                    errors.append("Tracking URL is missing.")
                if not tracking_id:
                    errors.append("Tracking ID is missing.")
                if not wolt_order_reference_id:
                    errors.append("Wolt order reference ID is missing.")

                if errors:
                    return redirect('basket')
                
                parsed_url = urlparse(tracking_url)
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    return redirect('basket')                    
                try:
                    basket_items = BasketItem.objects.filter(user=request.user)

                    if basket_items.count() == 0:
                        return redirect('basket')                    
                    for item in basket_items:
                        product = Product.objects.get(id=item.product.id)
                        if item.quantity > product.stock:
                            messages.error(request, f"Stokda '{product.title}' yoxdur.")
                            return redirect('basket')
                    total_amount = sum(item.total_price for item in basket_items)

                    coupon_code = transaction_obj.coupon_code
                    applied_coupon = None

                    if coupon_code:
                        try:
                            applied_coupon = Coupon.objects.get(coupon=coupon_code)
                            # Kuponun kullanılabilir olup olmadığını kontrol et
                            if not applied_coupon.can_user_use_coupon(request.user):
                                return redirect('basket')
                        
                        except Coupon.DoesNotExist:
                            return redirect('basket')
                    with transaction.atomic():
                        order = Order.objects.create(
                            user=request.user,
                            total_amount=total_amount,
                            discount=total_amount - apply_coupon(request.user, basket_items, applied_coupon) if applied_coupon else None,
                            discount_amount=apply_coupon(request.user, basket_items, applied_coupon) if applied_coupon else None,
                            coupon=applied_coupon,
                            tracking_url = tracking_url,
                            tracking_id = tracking_id,
                            wolt_order_reference_id = wolt_order_reference_id
                        )

                        for item in basket_items:
                            product = Product.objects.get(id=item.product.id)
                            OrderItem.objects.create(order=order, product=product, quantity=item.quantity)

                            product.stock -= item.quantity
                            product.save()

                    basket_items.delete()
                    if coupon_code:
                        coupon_usage = CouponUsage.objects.get(user=request.user, coupon=applied_coupon)
                        coupon_usage.max_coupon_usage_count -= 1
                        coupon_usage.save()
                    context["tracking_url"] = tracking_url
                except Exception as e:
                    print(e)
                    return  redirect('failed')
        else:
            try:
                basket_items = BasketItem.objects.filter(user=request.user)

                if basket_items.count() == 0:
                    return redirect('basket')
                
                # Stok kontrolü
                for item in basket_items:
                    product = Product.objects.get(id=item.product.id)
                    if item.quantity > product.stock:
                        messages.error(request, f"Stokda '{product.title}' yoxdur.")
                        return redirect('basket')

                # Toplam ücret hesapla
                total_amount = sum(item.total_price for item in basket_items)

                # Kupon işlemleri
                coupon_code = transaction_obj.coupon_code
                applied_coupon = None

                if coupon_code:
                    try:
                        applied_coupon = Coupon.objects.get(coupon=coupon_code)
                        # Kuponun kullanılabilir olup olmadığını kontrol et
                        if not applied_coupon.can_user_use_coupon(request.user):
                            return redirect('basket')
                    
                    except Coupon.DoesNotExist:
                        return redirect('basket')

                # İndirimli toplam tutarı hesapla

                # Sipariş oluştur
                with transaction.atomic():
                    order = Order.objects.create(
                        user=request.user,
                        total_amount=total_amount,  # İndirimli toplam tutarı kullan
                        discount=total_amount - apply_coupon(request.user ,basket_items, applied_coupon) if applied_coupon else None,
                        discount_amount = apply_coupon(request.user ,basket_items, applied_coupon) if applied_coupon else None,
                        coupon=applied_coupon,
                    )

                    # Siparişe ürünleri ekle ve stok güncelle
                    for item in basket_items:
                        product = Product.objects.get(id=item.product.id)
                        OrderItem.objects.create(order=order, product=product, quantity=item.quantity)

                        # Stok düşürme
                        product.stock -= item.quantity
                        product.save()

                # Sepeti temizle (veya kendi sepet yönetimine göre uyarla)
                basket_items.delete()
                if coupon_code:
                    coupon_usage = CouponUsage.objects.get(user=request.user, coupon = applied_coupon)
                    coupon_usage.max_coupon_usage_count -= 1
                    coupon_usage.save()
            except Exception as e:
                print(E)
                messages.error(request, 'Sifariş oluşturulurken bir hata oluştu.')
                return redirect('basket')
        transaction_obj.is_checked_from_eco = True
        transaction_obj.save()
        return render(request, 'success.html', context = context)
    elif response_data["status"] == 'new':
        context["payment_redirect_url"] = transaction_obj.payment_redirect_url
        return render(request, 'failed.html', context = context)
    return redirect('failed')

def failed(request):
    # transaction_obj = Transaction.objects.filter(user = request.user, ).last()
    return render(request, 'failed.html')

def result(request):
    return render(request, 'result.html')

def map(request):
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
        return delivery.shipment_promises()
    return JsonResponse({"message": "Please send lat and lon value"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_request_api_view(request):
    amount = request.data.get('amount')
    if not amount:
        return Response('Amount is missing')
    payment_obj = Payment()
    response = payment_obj.checkout_request(amount = amount)
    return Response(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deliveries(request):
    lat = request.data.get('lat')
    lon = request.data.get('lon')
    amount = request.data.get('amount')
    recipient_name = request.data.get('recipient_name')
    recipient_phone = request.data.get('recipient_phone')
    shipment_promise_id = request.data.get('shipment_promise_id')
    user_basket_items = BasketItem.objects.filter(user=request.user).order_by("pk")
    parcel_list = [item.to_dict_for_wolt_delivery() for item in user_basket_items]
    if lat and lon and amount and recipient_name and recipient_phone and parcel_list and shipment_promise_id:
        delivery = Delivery(lat = lat, lon = lon)
        return Response(delivery.deliveries(amount = amount, recipient_name = recipient_name, recipient_phone = recipient_phone, parcel_list = parcel_list, shipment_promise_id = shipment_promise_id))
    return Response({"message": "Please enter correct datas."})

class TransactionCreateAPIView(CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)