from apps.product.models import Order

class OrderRepository:
    DEFAULT_QS = Order.objects.all().order_by('-created_at')

    def __init__(self):
        self.model = Order

    def get_by_id(self, id, qs=DEFAULT_QS):
        return qs.filter(id=id)
    
    def get_all(self):
        return self.DEFAULT_QS