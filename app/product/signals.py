# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Company, Order
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()

@receiver(post_save, sender = Company)
def update_product_discount(sender, instance, **kwargs):
    if instance.product:
        instance.product.discount = instance.discount
        instance.product.save()

# @receiver(post_save, sender=Order)
# def send_order_email(sender, instance, created, **kwargs):
#     if created and instance.is_wolt:  # Yeni bir sipariş oluşturulduğunda işlevi çalıştırın
#         data = {
#             'order': instance,
#         }
       
#         message = render_to_string('mail.html', data)

#         send_mail(
#             "ecoproduct.az saytından Wolt kuriyer ilə sifariş var. Zəhmət olmasa 30 dəqiqə ərzində sifarişləri hazırlayın",
#             message,
#             settings.EMAIL_HOST_USER,
#             [settings.DEFAULT_FROM_EMAIL],
#             fail_silently=False, html_message=message
#         )   
       