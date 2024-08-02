import datetime
from django.contrib.sites.models import Site
from utils.time_helper.is_active_time import is_active_time

from apps.config.models.general_settings import *
from apps.product.models import *

def extras(request):
    general_setting = GeneralSettings.objects.first()
    site = Site.objects.get_current()
    site_url = site.domain
    
    # Using the is_active_time function
    is_active_time_value = is_active_time()

    context={
        'current_year': datetime.datetime.now().year,
        'current_time': datetime.datetime.now(),
        'is_active_time': is_active_time_value,
        'categories': ProductCategory.objects.all(),
        'setting': general_setting,
        'all_products': Product.objects.all(),
        'site_url': site_url,
        'header_companies': Company.objects.all()
    }
    if request.user.is_authenticated:
        context['favorite_count'] = Favorite.objects.filter(user=request.user).count()
    return context