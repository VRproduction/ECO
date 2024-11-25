from django.urls import path
from . import views

from .view_list.logix import test_logix_order


urlpatterns = [
    path('', views.payment, name = 'payment'),
    path('success/', views.SuccessView.as_view(), name = 'success'),
    # path('success/', views.result, name = 'success'),

    path('failed/', views.failed, name = 'failed'),
    path('result/', views.result, name = 'result'),
    path('map/', views.map, name = 'map'),
    path('map/shipment_promises/', views.shipment_promises, name = 'shipment_promises'),
    path('map/deliveries/', views.deliveries, name = 'deliveries'),
    path('checkout-request-api-view/', views.checkout_request_api_view, name = 'checkout_request_api_view'),
    path('transactions/', views.TransactionCreateAPIView.as_view()),

    path('test-logix/', test_logix_order, name='test_logix_order'),
]
