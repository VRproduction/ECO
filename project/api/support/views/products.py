from django.views.decorators.http import require_http_methods

from rest_framework import viewsets, permissions
from rest_framework.response import Response

from ..serializers.products import ProductSerializer, ProductCategorySerializer
from apps.product.models import Product, ProductCategory

from utils.api.mixins.api_key import APIKeyMixin
from utils.api.decorators.api_key import require_api_key

class ProductViewSet(APIKeyMixin, viewsets.ModelViewSet):
    
    allow_external = True  # Restrict access for external keys
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug' 

    def get_serializer_context(self):
        """Add request object to the serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class ProductCategoryViewSet(APIKeyMixin, viewsets.ModelViewSet):
    
    allow_external = True  # Restrict access for external keys
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    lookup_field = 'slug' 

