from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.products import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='api-product')
router.register(r'categories', ProductCategoryViewSet, basename='api-categories')

urlpatterns = [
    path('', include(router.urls)),
]
