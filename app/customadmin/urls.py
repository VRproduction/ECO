from django.urls import path, include


urlpatterns = [
    path('', include('customadmin.orders.urls'))
]