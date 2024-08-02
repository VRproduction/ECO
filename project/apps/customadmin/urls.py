from django.urls import path, include


urlpatterns = [
    path('', include('apps.customadmin.orders.urls')),
    path('api/', include('apps.customadmin.orders.api.urls'))
]