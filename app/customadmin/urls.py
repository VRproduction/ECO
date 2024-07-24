from django.urls import path, include


urlpatterns = [
    path('', include('customadmin.orders.urls')),
    path('api/', include('customadmin.orders.api.urls'))
]