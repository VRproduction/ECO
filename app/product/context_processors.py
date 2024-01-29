from .models import *
import datetime

def extras(request):
    context={
        'current_year': datetime.datetime.now().year,
    }
    if request.user.is_authenticated:
        context['favorite_count'] = Favorite.objects.filter(user = request.user).count()
    return context