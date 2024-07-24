from django.urls import path

from .views import OrderAdminListView, OrderDeleteView

urlpatterns = [
    path('orders/', OrderAdminListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDeleteView.as_view(), name='order-delete')
]