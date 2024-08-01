from celery import shared_task
from django.utils import timezone
from .models import Company

@shared_task
def remove_expired_discounts():
    now = timezone.now()
    companies = Company.objects.filter(finish_time__lt=now)
    for expired_company in companies:
        if expired_company.product:
            expired_company.product.discount = None
            expired_company.product.save()
