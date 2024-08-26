from celery import shared_task
from django.utils import timezone
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

@shared_task
def remove_expired_discounts(company_id):
    Company = apps.get_model('product', 'Company')
    try:
        expired_company = Company.objects.get(id=company_id)
    except ObjectDoesNotExist:
        return 'Company does not exist'

    if expired_company.finish_time <= timezone.now():
        if expired_company.product:
            expired_company.product.discount = None
            expired_company.product.save()
        return 'Discount removed'
    return 'No action needed'
