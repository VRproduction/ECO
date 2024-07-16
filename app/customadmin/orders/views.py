from django.views.generic import ListView

from product.models import Order

class OrderAdminListView(ListView):
    context_object_name = 'orders'
    paginate_by = 10
    template_name = 'orders/order-list.html'
    queryset = Order.objects.all()
