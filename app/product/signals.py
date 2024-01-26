# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Company

@receiver(post_save, sender = Company)
def update_product_discount(sender, instance, **kwargs):
    if instance.product:
        instance.product.discount = instance.discount
        instance.product.save()
