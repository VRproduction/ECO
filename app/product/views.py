from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from .models import FAQ, BasketItem, Blog, Favorite, IndexSlider, ProductCategory, Product, CategoryBanner, About, Feature, Company, Partner, Statistic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from account.utils.login_helper import AuthView, IsNotAuthView
from django.urls import reverse_lazy
from .forms import ContactForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.generic.edit import FormView

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["sliders"] = IndexSlider.objects.all()[:2]
        context["categories"] = ProductCategory.objects.all()
        context["products"] = Product.objects.filter(is_main_page = True).order_by("-badges")[:10]
        context["category_banners"] = CategoryBanner.objects.all()[:3]
        context["about"] = About.objects.first()
        context["features"] = Feature.objects.all()
        context["companies"] = Company.objects.filter(is_active = True)[:4]
        context["most_selling_products"] = Product.objects.all().order_by("?")[:3]
        context["most_search_products"] = Product.objects.all().order_by("?")[:3]
        context["trending_products"] = Product.objects.all().order_by("?")[:3]
        context["partners"] = Partner.objects.all()
        context["statistic"] = Statistic.objects.first()
        context["faqs"] = FAQ.objects.all()
        context["blogs"] = Blog.objects.filter(is_main_page = True)[:3]
        return context
    
class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context["about"] = About.objects.first()
        context["partners"] = Partner.objects.all()
        return context
    

class ShopPageView(ListView):
    template_name = 'shop.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        vendor_id = self.request.GET.get('vendor')
        ordering = self.request.GET.get('ordering')
        search_query = self.request.GET.get('search')

        queryset = Product.objects.all()

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category__id=int(category_id))

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if ordering:
            queryset = queryset.order_by(ordering)

        if vendor_id and vendor_id.isdigit():
            queryset = queryset.filter(vendor__id=int(vendor_id))

        return queryset
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('show', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category_id = self.request.GET.get('category')
        vendor_id = self.request.GET.get('vendor')
        ordering = self.request.GET.get('ordering')
        search_query = self.request.GET.get('search')

        queryset = Product.objects.all()

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category__id=int(category_id))

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if ordering:
            queryset = queryset.order_by(ordering)

        if vendor_id and vendor_id.isdigit():
            queryset = queryset.filter(vendor__id=int(vendor_id))

        context["count"] = queryset.count()
        context["categories"] = ProductCategory.objects.all()
        context["new_products"] = Product.objects.all().order_by("-id")[:3]
        context["companies"] = Company.objects.filter(is_active=True)[:4]
        return context

class BasketPageView(TemplateView, IsNotAuthView):
    template_name = 'basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = BasketItem.objects.filter(user = self.request.user).order_by("pk")
        return context

def round_to_decimal(value):
    try:
        rounded_value = round(float(value), 2)
        
        rounded_value_str = "{:,.{decimal_places}f}".format(rounded_value, decimal_places=2).replace(',', '.')

        return rounded_value_str
    except (ValueError, TypeError):
        return value

def get_basket_items(request):
    try:
        # Kullanıcıya ait sepet öğelerini al
        basket_items = BasketItem.objects.filter(user=request.user).order_by("pk")
        
        # Sepet içeriğini JSON formatında döndür
        basket_items_data = [{
            'id': item.id,
            'product': {
                'id': item.product.pk,
                'title': item.product.title,
                'price': round_to_decimal(item.product.price),
                'image_url': item.product.image.url,
            },
            'quantity': item.quantity,
            'total_price': round_to_decimal(item.total_price),
        } for item in basket_items]

        response_data = {
            'basketItemCount': basket_items.count(),
            'basketItems': basket_items_data,
            'totalPrice': round_to_decimal(sum(item.total_price for item in basket_items)),
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_basket(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        quantity = int(request.data.get('quantity', 1))  # Default quantity is 1 if not provided
        basket_item, created = BasketItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            basket_item.quantity += quantity
            basket_item.save()
        else:
            basket_item.quantity = quantity
            basket_item.save()

        return Response({'success': True, 'message': f"{quantity} added to the basket."})
    
    except Product.DoesNotExist:
        return Response({'success': False, 'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def remove_from_basket(request, basket_item_id):
    try:
        basket_item = BasketItem.objects.get(pk=basket_item_id, user=request.user)
        basket_item.delete()

        return JsonResponse({'success': True, 'message': "Ürün sepetten kaldırıldı."})

    except BasketItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Ürün bulunamadı.'}, status=404)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_basket_item_count(request, product_id):
    # Get the product and user from the request
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Check if the basket item already exists for the user and product
    basket_item, created = BasketItem.objects.get_or_create(user=user, product=product)

    # Get the quantity change from the JSON data
    quantity_change = request.data.get('quantity_change')

    # Update the quantity based on the quantity_change
    if quantity_change is not None and isinstance(quantity_change, int):
        basket_item.quantity += quantity_change
        if basket_item.quantity <= 0:
            basket_item.delete()
        else:
            basket_item.save()
    else:
        return JsonResponse({'error': 'Invalid quantity_change'}, status=400)

    # Return the updated basket item count in the JsonResponse
    response_data = {
        'basket_item_count': BasketItem.objects.filter(user=user).count(),
    }

    return JsonResponse(response_data)

def clear_basket(request):
    user = request.user

    # Delete all basket items for the user
    BasketItem.objects.filter(user=user).delete()

    # Return success message and updated basket item count
    response_data = {
        'success': True,
        'message': 'Basket cleared successfully',
        'basket_item_count': BasketItem.objects.filter(user=user).count(),
    }

    return JsonResponse(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_selected_basket_items(request):
    user = request.user
    selected_item_ids = request.data.get('selected_items', [])

    # Delete selected basket items for the user
    BasketItem.objects.filter(user=user, id__in=selected_item_ids).delete()

    # Return success message and updated basket item count
    response_data = {
        'success': True,
        'message': 'Selected basket items deleted successfully',
        'basket_item_count': BasketItem.objects.filter(user=user).count(),
    }

    return Response(response_data, status=status.HTTP_200_OK)

class WishListPageView(TemplateView, IsNotAuthView):
    template_name = 'wish_list.html'

    def get_context_data(self, **kwargs):
        context = super(WishListPageView, self).get_context_data(**kwargs)
        context["products"] = Product.objects.filter(favorites__user=self.request.user)
        return context
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, product_id):
    user = request.user

    try:
        favorite = Favorite.objects.get(product_id=product_id, user=user)
        favorite.delete()  # Eğer favoride ise kaldır
        return Response({'success': True, 'action': 'removed'}, status=status.HTTP_200_OK)
    except Favorite.DoesNotExist:
        # Eğer favoride değilse ekleyin
        Favorite.objects.create(product_id=product_id, user=user)
        return Response({'success': True, 'action': 'added'}, status=status.HTTP_200_OK)
    
class BlogPageView(TemplateView):
    template_name = 'blogs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all()
        return context
    
class BlogDetailPageView(DetailView):
    template_name = 'blog-detail.html'
    model = Blog
    context_object_name = "blog"
    
    def get_context_data(self, **kwargs):
        context = super(BlogDetailPageView, self).get_context_data(**kwargs)
        context["last_blogs"] = Blog.objects.exclude(pk = self.get_object().pk).order_by("-created")[:3]
        return context
    
    
class CompanyPageView(TemplateView):
    template_name = 'companies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.all()
        return context
    
class ContactPageView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Mesajınız göndərildi!')
        return super().form_valid(form)
    
class AccountPageView(TemplateView, IsNotAuthView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context