from .models import *
import datetime
from django.contrib.sites.models import Site

def extras(request):
    site = Site.objects.get_current()
    site_url = site.domain
    context={
        'current_year': datetime.datetime.now().year,
        'categories': ProductCategory.objects.all(),
        'setting': GeneralSettings.objects.first(),
        'all_products': Product.objects.all(),
        'site_url': site_url
    }
    if request.user.is_authenticated:
        context['favorite_count'] = Favorite.objects.filter(user = request.user).count()
    return context