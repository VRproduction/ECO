
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from ..serializers.products import ProductSerializer, ProductCategorySerializer
from apps.product.models import Product, ProductCategory

from utils.api.mixins.api_key import APIKeyMixin
from utils.api.decorators.api_key import require_api_key
from utils.api.pagination.limit_of_set_pagination import CustomLimitOffsetPagination

class ProductViewSet(APIKeyMixin, viewsets.ModelViewSet):
    
    allow_external = True  # Restrict access for external keys
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug' 
    pagination_class = CustomLimitOffsetPagination
    
    def get_serializer_context(self):
        """Add request object to the serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    
    @extend_schema(
        description="Create one or more items.",
        examples=[
            OpenApiExample(
                'Single Item Request',
                value={
                    "title": "string",
                    "category": "string",  # Example category name
                    "price": 0,
                    "stock": 0
                },
                request_only=True,
                response_only=False
            ),
            OpenApiExample(
                'Multiple Item Request',
                value=(
                    {
                        "title": "string",
                        "category": "string",  # Example category name
                        "price": 0,
                        "stock": 0
                    },
                    {
                        "title": "string",
                        "category": "string",  # Example category name
                        "price": 0,
                        "stock": 0
                    },
                ),
                request_only=True,
                response_only=False

            )
        ],
        
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        errors = []
        
        if isinstance(data, list):
            serializers = []
            
            # Collect all titles to check for duplicates
            titles = [item.get('title', 'No Title') for item in data]
            duplicate_titles = [title for title in set(titles) if titles.count(title) > 1]
            
            if duplicate_titles:
                return Response({
                    'error': f'Duplicate product titles found: {", ".join(duplicate_titles)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate all items first
            for item in data:
                serializer = self.get_serializer(data=item)
                if serializer.is_valid():
                    serializers.append(serializer)
                else:
                    # Collect all errors with title reference
                    title = item.get('title', 'No Title')
                    errors.append({
                        'title': title,
                        'errors': serializer.errors
                    })

            # If there are errors, raise ValidationError and do not create any objects
            if errors:
                raise ValidationError({'errors': errors})

            # If all items are valid, create them
            for serializer in serializers:
                self.perform_create(serializer)
            
            return Response([serializer.data for serializer in serializers], status=status.HTTP_201_CREATED)
        
        else:
            # Handle single creation
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class ProductCategoryViewSet(APIKeyMixin, viewsets.ModelViewSet):
    
    allow_external = True  # Restrict access for external keys
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    lookup_field = 'slug' 

