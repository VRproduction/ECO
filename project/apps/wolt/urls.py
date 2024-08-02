from django.urls import path
from .views import shipment_promises

urlpatterns = [
    path('shipment-promises/', shipment_promises, name='shipment_promises'),
]
