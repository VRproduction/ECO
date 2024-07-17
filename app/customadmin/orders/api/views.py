from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .serializers import (
    OrderListSerializer,
    OrderRetrieveUpdateDestroySerializer
)

from.repositories import OrderRepository
from product.models import Order, OrderItem


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all().order_by('-created_at')
    repo = OrderRepository

    def get_filter_methods(self):
        repo = self.repo()
        return {
            'id' : repo.get_by_id,
        }

    def get_queryset(self, **kwargs):
        qs = super().get_queryset() 
        filters = self.get_filter_methods()
        
        for key, value in self.request.query_params.items():
            if key in filters:
                qs = filters[key](value, qs)
        return qs
    

class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderRetrieveUpdateDestroySerializer
    queryset = Order.objects.all().order_by('-created_at')