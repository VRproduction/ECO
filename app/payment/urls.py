from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name = 'payment'),
    path('success/', views.success, name = 'success'),
    path('failed/', views.failed, name = 'failed'),
    path('result/', views.result, name = 'result'),
    path('map/', views.map, name = 'map'),
    path('map/shipment_promises/', views.shipment_promises, name = 'shipment_promises'),
    path('map/deliveries/', views.deliveries, name = 'deliveries'),
]