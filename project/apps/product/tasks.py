from celery import shared_task
from django.utils import timezone
from .models import Company

@shared_task
def remove_expired_discounts(company_id):
    expired_company = Company.objects.get(id=company_id)
    print(expired_company)
    if expired_company.product:
        expired_company.product.discount = None
        expired_company.product.save()
    return 'ok'