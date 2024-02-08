from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from .models import FAQ, BasketItem, Blog, ContactPage, CouponUsage, Favorite, IndexSlider, Order, OrderItem, ProductCategory, Product, CategoryBanner, About, Feature, Company, Partner, Statistic, Coupon
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from account.utils.login_helper import AuthView, IsNotAuthView
from django.urls import reverse_lazy
from .forms import AccountUpdateForm, ContactForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.generic.edit import FormView
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["sliders"] = IndexSlider.objects.all()[:1]
        context["categories"] = ProductCategory.objects.all()
        context["products"] = Product.objects.filter(is_main_page = True).order_by("-badges")[:10]
        context["category_banners"] = CategoryBanner.objects.all()[:3]
        context["about"] = About.objects.first()
        context["features"] = Feature.objects.all()
        context["companies"] = Company.objects.filter(finish_time__gte=datetime.datetime.now())[:4]
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
        context["companies"] = Company.objects.filter(finish_time__gte=datetime.datetime.now())[:4]
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

def apply_coupon(user, basket_items, coupon):
    basket_total = sum(item.total_price for item in basket_items)
    discounted_total = coupon.apply_discount(user, basket_total)
    return discounted_total

def get_basket_items(request):
    try:
        # Kullanıcıya ait sepet öğelerini al
        basket_items = BasketItem.objects.filter(user=request.user).order_by("pk")
        
        coupon_code = request.GET.get('coupon_code', None)
        
        # Sepet içeriğini JSON formatında döndür
        basket_items_data = [{
            'id': item.id,
            'product': {
                'id': item.product.pk,
                'title': item.product.title,
                'price': round_to_decimal(item.product.discount_price) if item.product.discount else round_to_decimal(item.product.price),
                'image_url': item.product.image.url,
            },
            'quantity': item.quantity,
            'total_price': round_to_decimal(item.total_price),
        } for item in basket_items]
        
        basket_total = sum(item.total_price for item in basket_items)

    
        response_data = {
            'basketItemCount': basket_items.count(),
            'basketItems': basket_items_data,
            'totalPrice': round_to_decimal(basket_total),
        }
        applied_coupon = None

        if coupon_code:
            try:
                applied_coupon = Coupon.objects.get(coupon=coupon_code)
                # Kuponun kullanılabilir olup olmadığını kontrol et
            except Coupon.DoesNotExist:
                response_data['error'] = 'Kupon mövcud deyil!'
                return JsonResponse(response_data)
        if applied_coupon:
            discounted_total = apply_coupon(request.user ,basket_items, applied_coupon)
            response_data["discountPrice"] = round_to_decimal(discounted_total)
            response_data["discount"] = round_to_decimal(basket_total - discounted_total),

        return JsonResponse(response_data)

    except Exception as e:
        response_data['error'] = 'Siz artıq bu kuponu istifadə etmisiz!'
        return JsonResponse(response_data)

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


# def checkout(request):
#     basket_items = BasketItem.objects.filter(user=request.user)
#     # Stok kontrolü
#     for item in basket_items:
#         product = Product.objects.get(id=item.product.id)
#         if item.quantity > product.stock:
#             messages.error(request, f"Not enough stock for {product.title}.")
#             return redirect('basket')

#     total_amount =  sum(item.total_price for item in basket_items)
#     order = Order.objects.create(user=request.user, total_amount=total_amount)

#     # Siparişe ürünleri ekleyin ve stok güncelleyin
#     for item in basket_items:
#         product = Product.objects.get(id=item.product.id)
#         OrderItem.objects.create(order=order, product=product, quantity=item.quantity)

#         # Stok düşürme
#         product.stock -= item.quantity
#         product.save()

#     # Sepeti temizleme (veya kendi sepet yönetimine göre uyarla)
#     basket_items.delete()

#     return redirect('basket')

from django.db import transaction

@transaction.atomic
def checkout(request):
    try:
        basket_items = BasketItem.objects.filter(user=request.user)

        if basket_items.count() == 0:
            messages.error(request, 'Səbətdə məhsul yoxdur!')
            return redirect('basket')
        
        # Stok kontrolü
        for item in basket_items:
            product = Product.objects.get(id=item.product.id)
            if item.quantity > product.stock:
                messages.error(request, f"Stokda '{product.title}' yoxdur.")
                return redirect('basket')

        # Toplam ücret hesapla
        total_amount = sum(item.total_price for item in basket_items)

        # Kupon işlemleri
        coupon_code = request.GET.get('coupon_code')
        applied_coupon = None

        if coupon_code:
            try:
                applied_coupon = Coupon.objects.get(coupon=coupon_code)
                # Kuponun kullanılabilir olup olmadığını kontrol et
                if not applied_coupon.can_user_use_coupon(request.user):
                    messages.error(request, 'Siz artıq bu kuponu istifadə etmisiz!')
                    return redirect('basket')
              
            except Coupon.DoesNotExist:
                messages.error(request, 'Kupon mövcud deyil!')
                return redirect('basket')

        # İndirimli toplam tutarı hesapla

        # Sipariş oluştur
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,  # İndirimli toplam tutarı kullan
                discount=total_amount - apply_coupon(request.user ,basket_items, applied_coupon) if applied_coupon else None,
                discount_amount = apply_coupon(request.user ,basket_items, applied_coupon) if applied_coupon else None,
                coupon=applied_coupon,
            )

            # Siparişe ürünleri ekle ve stok güncelle
            for item in basket_items:
                product = Product.objects.get(id=item.product.id)
                OrderItem.objects.create(order=order, product=product, quantity=item.quantity)

                # Stok düşürme
                product.stock -= item.quantity
                product.save()

        # Sepeti temizle (veya kendi sepet yönetimine göre uyarla)
        basket_items.delete()
        if coupon_code:
            coupon_usage = CouponUsage.objects.get(user=request.user, coupon = applied_coupon)
            coupon_usage.max_coupon_usage_count -= 1
            coupon_usage.save()
        messages.success(request, 'Siparişiniz uğurla qeydə alındı.')
        return redirect('basket')

    except Exception as e:
        messages.error(request, 'Sipariş oluşturulurken bir hata oluştu.')
        return redirect('basket')


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
        context["companies"] = Company.objects.filter(finish_time__gte=datetime.datetime.now())
        return context
    
class ContactPageView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Mesajınız göndərildi!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = ContactPage.objects.first()
        return context
    

class AccountPageView(TemplateView, IsNotAuthView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(user=self.request.user)
        context["form"] = AccountUpdateForm(instance=self.request.user)
        context["password_form"] = PasswordChangeForm(user=self.request.user)
        
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST.get("submit") == 'account_submit':
            form = AccountUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(self.request, 'Hesab məlumatları uğurla yeniləndi!')
            else:
                messages.error(self.request, 'Məlumatları düzgün daxil edin!')
            context = self.get_context_data()
            context['form'] = form
            context['tab'] = 2
            return self.render_to_response(context)
        elif request.POST.get("submit") == 'password_submit':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Oturumu güncelle
                messages.success(request, 'Parol uğurla dəyişdirildi!')
            else:
                messages.error(self.request, 'Parolu düzgün daxil edin!')
            context = self.get_context_data()
            context['tab'] = 3
            return self.render_to_response(context)


