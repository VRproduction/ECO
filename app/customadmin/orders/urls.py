from django.urls import path, include
from .views import OrderAdminListView

urlpatterns = [
    path('orders/', OrderAdminListView.as_view(), name='order-list')
]