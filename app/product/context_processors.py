from .models import *
import datetime
from django.contrib.sites.models import Site

def extras(request):
    general_setting = GeneralSettings.objects.first()
    site = Site.objects.get_current()
    site_url = site.domain
    if datetime.datetime.now().minute == 0:
        if general_setting.work_start_hour.hour <= datetime.datetime.now().hour <= general_setting.work_finish_hour.hour:
            is_active_time = True
        else:
            is_active_time = False
    else:
        if general_setting.work_start_hour.hour < datetime.datetime.now().hour < general_setting.work_finish_hour.hour:
            is_active_time = True
        else:
            is_active_time = False
    print(general_setting.work_finish_hour.hour)
    context={
        'current_year': datetime.datetime.now().year,
        'current_time': datetime.datetime.now(),
        'is_active_time': is_active_time,
        'categories': ProductCategory.objects.all(),
        'setting': general_setting,
        'all_products': Product.objects.all(),
        'site_url': site_url,
        'header_companies': Company.objects.all()
    }
    if request.user.is_authenticated:
        context['favorite_count'] = Favorite.objects.filter(user = request.user).count()
    return context