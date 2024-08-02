from typing import Any
from django.db.models import Q
from django.views.generic import (
    ListView, 
    DeleteView
)

from apps.product.models import Order
from .utils import SuperuserRequiredMixin


class OrderAdminListView(SuperuserRequiredMixin, ListView):
    context_object_name = 'orders'
    paginate_by = 10
    template_name = 'orders/order-list.html'
    queryset = Order.objects.all()

    def get_context_data(self, **kwargs):
        order_types = [
            'Yeni',
            'Paketlənən',
            'Təhvilə hazır',
            'Tamamlanmış',
            'Ləğv edilib'
        ]
        cx = super().get_context_data(**kwargs)
        cx['order_types'] = order_types
        cx['orders_count'] = self.get_queryset().count()
        return cx
    
    def get_queryset(self):
        queryset = Order.objects.all()
        order_type = self.request.GET.get('order_type')
        query = self.request.GET.get('query')

        if order_type:
            queryset = queryset.filter(order_type=order_type)
        
        if query:
            queryset = queryset.filter(
                Q(user__email__icontains=query) |
                Q(order_type=query) |
                Q(order_items__product__title=query)
            )

        return queryset

    
class OrderDeleteView(DeleteView, SuperuserRequiredMixin):
    model = Order
    template_name = 'orders/order-list.html'
    success_url = '/custom-admin/orders'
    login_url = "/"