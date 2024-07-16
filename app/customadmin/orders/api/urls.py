from django.urls  import path

from .views import (
    OrderListAPIView,
    OrderRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('orders/', OrderListAPIView.as_view(), name='order-list-api'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-update-destroy')
]