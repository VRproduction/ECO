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

@transaction.atomic
@login_required
def success(request):
    context = {

    }
    user = request.user
    transaction_obj = Transaction.objects.filter(user = user).last()
    payment_obj = Payment()
    response_data = payment_obj.get_payment_status(transaction_obj)  
    if response_data["status"] == 'success' and not transaction_obj.is_checked_from_eco:
        # try:
            basket_items = BasketItem.objects.filter(user=user)

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
                    if not applied_coupon.can_user_use_coupon(user):
                        return redirect('basket')
                    
                except Coupon.DoesNotExist:
                    return redirect('basket')

                # İndirimli toplam tutarı hesapla

            # Sipariş oluştur
            with transaction.atomic():
                if transaction_obj.is_wolt:
                    order = Order.objects.create(
                    user=user,
                    total_amount=total_amount + (transaction_obj.delivery_amount if total_amount < 30 else 0),  # İndirimli toplam tutarı kullan
                    discount=total_amount - apply_coupon(user ,basket_items, applied_coupon) if applied_coupon else None,
                    discount_amount = apply_coupon(user ,basket_items, applied_coupon)+(transaction_obj.delivery_amount if apply_coupon(user ,basket_items, applied_coupon) < 30 else 0) if applied_coupon else None ,
                    delivery_amount = transaction_obj.delivery_amount,
                    is_delivery_free = (applied_coupon and apply_coupon(user ,basket_items, applied_coupon) > 30 and apply_coupon(user ,basket_items, applied_coupon)) or (total_amount > 30 and total_amount is not None), 
                    coupon=applied_coupon ,
                    is_wolt = True,
                    transaction = transaction_obj
                )
                else:
                    order = Order.objects.create(
                        user=user,
                        total_amount=total_amount,  # İndirimli toplam tutarı kullan
                        discount=total_amount - apply_coupon(user ,basket_items, applied_coupon) if applied_coupon else None,
                        discount_amount = apply_coupon(user ,basket_items, applied_coupon) if applied_coupon else None,
                        coupon=applied_coupon,
                        transaction = transaction_obj
                    )

                # Siparişe ürünleri ekle ve stok güncelle
                for item in basket_items:
                    product = Product.objects.get(id=item.product.id)
                    OrderItem.objects.create(order=order, product=product, quantity=item.quantity)

                    # Stok düşürme
                    product.stock -= item.quantity
                    product.sale_count += item.quantity
                    product.save()

                # Sepeti temizle (veya kendi sepet yönetimine göre uyarla)
            basket_items.delete()
            if coupon_code:
                coupon_usage = CouponUsage.objects.get(user=user, coupon = applied_coupon)
                coupon_usage.max_coupon_usage_count -= 1
                coupon_usage.save()
        # except Exception as e:
        #     print(e)
        #     messages.error(request, 'Sifariş oluşturulurken bir hata oluştu.')
        #     return redirect('basket')
            transaction_obj.is_checked_from_eco = True
            transaction_obj.save()
            return render(request, 'success.html', context = context)            
    elif response_data["status"] == 'new':
        context["payment_redirect_url"] = transaction_obj.payment_redirect_url
        return render(request, 'failed.html', context = context)
    return redirect('failed')


# @transaction.atomic
# @login_required
# def success(request):
#         context = {

#     }
#         transaction_obj = Transaction.objects.filter(user = request.user).last()
#     # try:
#         basket_items = BasketItem.objects.filter(user=request.user)

#         if basket_items.count() == 0:
#             return redirect('basket')
                
#             # Stok kontrolü
#         for item in basket_items:
#             product = Product.objects.get(id=item.product.id)
#             if item.quantity > product.stock:
#                 messages.error(request, f"Stokda '{product.title}' yoxdur.")
#                 return redirect('basket')

#             # Toplam ücret hesapla
#         total_amount = sum(item.total_price for item in basket_items)

#             # Kupon işlemleri
#         coupon_code = transaction_obj.coupon_code
#         applied_coupon = None

#         if coupon_code:
#             try:
#                 applied_coupon = Coupon.objects.get(coupon=coupon_code)
#                 # Kuponun kullanılabilir olup olmadığını kontrol et
#                 if not applied_coupon.can_user_use_coupon(request.user):
#                     return redirect('basket')
                    
#             except Coupon.DoesNotExist:
#                 return redirect('basket')

#                 # İndirimli toplam tutarı hesapla

#             # Sipariş oluştur
#         with transaction.atomic():
#             if transaction_obj.is_wolt:
#                 order = Order.objects.create(
#                     user=request.user,
#                     total_amount=total_amount + (transaction_obj.delivery_amount if total_amount < 30 else 0),  # İndirimli toplam tutarı kullan
#                     discount=total_amount - apply_coupon(request.user ,basket_items, applied_coupon) if applied_coupon else None,
#                     discount_amount = apply_coupon(request.user ,basket_items, applied_coupon)+(transaction_obj.delivery_amount if apply_coupon(request.user ,basket_items, applied_coupon) < 30 else 0) if applied_coupon else None ,
#                     delivery_amount = transaction_obj.delivery_amount,
#                     is_delivery_free = (applied_coupon and (request.user ,basket_items, applied_coupon) > 30 and apply_coupon(request.user ,basket_items, applied_coupon)) or (total_amount > 30 and total_amount is not None), 
#                     coupon=applied_coupon ,
#                     is_wolt = True,
#                     transaction = transaction_obj
#                 )
#             else:
#                 order = Order.objects.create(
#                     user=request.user,
#                     total_amount=total_amount,  # İndirimli toplam tutarı kullan
#                     discount=total_amount - apply_coupon(request.user ,basket_items, applied_coupon) if applied_coupon else None,
#                     discount_amount = apply_coupon(request.user ,basket_items, applied_coupon) if applied_coupon else None,
#                     coupon=applied_coupon,
#                     transaction = transaction_obj
#                 )

#             # Siparişe ürünleri ekle ve stok güncelle
#             for item in basket_items:
#                 product = Product.objects.get(id=item.product.id)
#                 OrderItem.objects.create(order=order, product=product, quantity=item.quantity)

#                 # Stok düşürme
#                 product.stock -= item.quantity
#                 product.sale_count += item.quantity
#                 product.save()

#                 # Sepeti temizle (veya kendi sepet yönetimine göre uyarla)
#         basket_items.delete()
#         if coupon_code:
#             coupon_usage = CouponUsage.objects.get(user=request.user, coupon = applied_coupon)
#             coupon_usage.max_coupon_usage_count -= 1
#             coupon_usage.save()
#     # except Exception as e:
#     #     print(e)
#     #     messages.error(request, 'Sifariş oluşturulurken bir hata oluştu.')
#     #     return redirect('basket')
#         transaction_obj.is_checked_from_eco = True
#         transaction_obj.save()
#         return render(request, 'success.html', context = context)            
    


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
        return delivery.shipment_promises()
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