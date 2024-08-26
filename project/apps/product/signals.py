from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib import messages
from urllib.parse import urlparse

from apps.payment.delivery.wolt import Delivery
from apps.config.models.general_settings import (
    PhoneNumber, 
    GeneralSettings
)
from .models import Company, Order, OrderItem
from .models import Coupon, CouponUsage



User = get_user_model()

@receiver(post_save, sender=User)
def create_coupon_usage_for_new_user(sender, instance, created, **kwargs):
    if created:
        coupons = Coupon.objects.all()
        for coupon in coupons:
            CouponUsage.objects.get_or_create(user=instance, coupon=coupon, defaults={'max_coupon_usage_count': 1})

@receiver(post_save, sender = Company)
def update_product_discount(sender, instance, **kwargs):
    if instance.product:
        instance.product.discount = instance.discount
        instance.product.save()

@receiver(post_save, sender=Company)
def handle_company_save(sender, instance, **kwargs):
    instance.schedule_discount_removal()

# @receiver(post_save, sender=Order)
# def send_order_email(sender, instance, created, **kwargs):
#     if created: 
#         choices = [
#             ('Gözləmədə', 'Gözləmədə'),
#             ('Hazırlandı', 'Hazırlandı'),
#             ('Göndərilib', 'Göndərilib'),
#             ('Çatdırılıb', 'Çatdırılıb'),
#             ('Ləğv edilib', 'Ləğv edilib'),
#         ]
#         for choice_value, choice_label in choices:
#             status = Status.objects.create(status=choice_value, order=instance)
#             if choice_value == 'Gözləmədə':
#                 status.is_confirmed = True
#                 status.save()

#         site = Site.objects.get_current()
#         site_url = site.domain
#         data = {
#             'order': instance,
#             'site_url': site_url,
#         }
#         if instance.is_wolt:
#             title = "Ecoproduct.az, sizə sifariş var! (kuryerlə çatdırılma)"
#         else:
#             title = "Ecoproduct.az, sizə sifariş var! (yerində ödəmə)"

#         message = render_to_string('mail/index.html', data)

#         send_mail(
#             title, 
#             message,
#             settings.EMAIL_HOST_USER,
#             [settings.DEFAULT_FROM_EMAIL],
#             fail_silently=False, html_message=message
#         )   


@receiver(post_save, sender=Order)
def send_order_email(sender, instance, created, **kwargs):
    if created: 
        site = Site.objects.get_current()
        site_url = site.domain
        data = {
            'order': instance,
            'site_url': site_url,
        }
        if instance.is_wolt:
            title = "Ecoproduct.az, sizə sifariş var! (kuryerlə çatdırılma)"
        else:
            title = "Ecoproduct.az, sizə sifariş var! (yerində ödəmə)"

        message = render_to_string('mail/index.html', data)

        send_mail(
            title, 
            message,
            settings.EMAIL_HOST_USER,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False, html_message=message
        ) 


@receiver(pre_save, sender=Order)
def send_order_ready_email(sender, instance, **kwargs):
    if instance.order_type == 'Təhvilə hazır':
        order = instance
        setting = GeneralSettings.objects.first()
        adress = setting.adress
        number = PhoneNumber.objects.filter(setting=setting, is_main=True).first().number

        if order.transaction.is_wolt:
            user_order_items = OrderItem.objects.filter(order=order).order_by("pk")
            parcel_list = [item.to_dict_for_wolt_delivery() for item in user_order_items]
            delivery = Delivery(lat=order.transaction.lat, lon=order.transaction.lon)
            delivery_response = delivery.deliveries(amount=order.transaction.delivery_amount,
                                                    recipient_name=order.transaction.recipient_name,
                                                    recipient_phone=order.transaction.recipient_phone,
                                                    dropoff_comment=order.transaction.dropoff_comment,
                                                    parcel_list=parcel_list,
                                                    shipment_promise_id=order.transaction.shipment_promise_id)
            print(delivery_response)
            
            if "error_code" in delivery_response:
                # Handle error scenario
                pass
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
                    return HttpResponseRedirect(reverse('admin:index'))
                
                parsed_url = urlparse(tracking_url)
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    return redirect('basket')  
                
                # Save the extracted data to the Order instance
                order.tracking_url = tracking_url
                order.tracking_id = tracking_id
                order.wolt_order_reference_id = wolt_order_reference_id
                

        if order.transaction.is_wolt:
            message = f'''Salam, ecoproduct.az-dan sifarişiniz artıq hazırdır. 
Qısa zaman ərzində kuryer vasitəsilə çatdırılacaq.

Əlaqə: 
📍{adress}
📞{number}'''

        else:
            message = f'''Salam, ecoproduct.az-dan sifarişiniz artıq hazırdır.
Ofisimizə yaxınlaşaraq sifarişinizi təhvil ala bilərsiniz.

Əlaqə: 
📍{adress}
📞{number}'''

        send_mail(
            "ecoproduct.az-dan sifarişiniz təsdiqləndi.",
            message,
            settings.EMAIL_HOST_USER,
            [order.user.email],
            fail_silently=False
        )


# @receiver(post_save, sender=Status)
# def send_order_ready_email(sender, instance, created, **kwargs):
#     if not created and instance.status == 'Hazırlandı' and instance.is_confirmed:
#         order = instance.order
#         setting = GeneralSettings.objects.first()
#         adress = setting.adress
#         number = PhoneNumber.objects.filter(setting=setting, is_main=True).first().number

#         if order.transaction.is_wolt:
#             user_order_items = OrderItem.objects.filter(order=order).order_by("pk")
#             parcel_list = [item.to_dict_for_wolt_delivery() for item in user_order_items]
#             delivery = Delivery(lat=order.transaction.lat, lon=order.transaction.lon)
#             delivery_response = delivery.deliveries(amount=order.transaction.amount,
#                                                     recipient_name=order.transaction.recipient_name,
#                                                     recipient_phone=order.transaction.recipient_phone,
#                                                     dropoff_comment=order.transaction.dropoff_comment,
#                                                     parcel_list=parcel_list,
#                                                     shipment_promise_id=order.transaction.shipment_promise_id)
#             if "error_code" in delivery_response:
#                 print(delivery_response["error_code"])
#                 # pul qaytarilmali olan funksiya
#                 return redirect('failed')
#             elif 'tracking' in delivery_response:
#                 tracking_url = delivery_response["tracking"]["url"]
#                 tracking_id = delivery_response["tracking"]["id"]
#                 wolt_order_reference_id = delivery_response["wolt_order_reference_id"]
                    
#                 errors = []

#                 if not tracking_url:
#                     errors.append("Tracking URL is missing.")
#                 if not tracking_id:
#                     errors.append("Tracking ID is missing.")
#                 if not wolt_order_reference_id:
#                     errors.append("Wolt order reference ID is missing.")

#                 if errors:
#                     return HttpResponseRedirect(reverse('admin:index'))
                
#                 parsed_url = urlparse(tracking_url)
#                 if not all([parsed_url.scheme, parsed_url.netloc]):
#                     return redirect('basket')  
#                 instance.order.tracking_url = tracking_url
#                 instance.order.tracking_id = tracking_id
#                 instance.order.wolt_order_reference_id = wolt_order_reference_id
#                 instance.order.save()
                
                
#         if order.transaction.is_wolt:
#             message = f'''Salam, ecoproduct.az-dan sifarişiniz artıq hazırdır. 
# Qısa zaman ərzində kuryer vasitəsilə çatdırılacaq.

# Əlaqə: 
# 📍{adress}
# 📞{number}'''

#         else:
#             message = f'''Salam, ecoproduct.az-dan sifarişiniz artıq hazırdır.
# Ofisimizə yaxınlaşaraq sifarişinizi təhvil ala bilərsiniz.

# Əlaqə: 
# 📍{adress}
# 📞{number}'''
#         send_mail(
#             "ecoproduct.az-dan sifarişiniz təsdiqləndi.",
#             message,
#             settings.EMAIL_HOST_USER,
#             [order.user.email],
#             fail_silently=False
#         )