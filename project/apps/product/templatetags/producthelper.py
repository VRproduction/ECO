from django import template
from apps.product.models import Product

register = template.Library()


@register.filter
def is_wished(product, request):
    return product in Product.objects.filter(favorites__user=request.user)