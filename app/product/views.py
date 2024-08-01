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
from urllib.parse import urlparse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from seo.models import AboutPageSeo, BlogPageSeo, ShopPageSeo, HomePageSeo, ContactPageSeo, CompaniesPageSeo
from django.utils.translation import get_language
from django.utils.translation import gettext as _

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["sliders"] = IndexSlider.objects.all()
        context["categories"] = ProductCategory.objects.all()
        context["products"] = Product.objects.filter(is_main_page = True, stock__gt=0).order_by("-badges")[:10]
        context["category_banners"] = CategoryBanner.objects.all()[:3]
        context["about"] = About.objects.first()
        context["features"] = Feature.objects.all()
        context["companies"] = Company.objects.filter(finish_time__gte=datetime.datetime.now())[:4]
        context["most_selling_products"] = Product.objects.filter(is_best_seller = True).order_by("?")[:3]
        context["most_search_products"] = Product.objects.filter(is_most_wonted = True).order_by("?")[:3]
        context["trending_products"] = Product.objects.filter(is_trending = True).order_by("?")[:3]
        context["partners"] = Partner.objects.all()
        context["statistic"] = Statistic.objects.first()
        context["faqs"] = FAQ.objects.all()
        context["blogs"] = Blog.objects.filter(is_main_page = True)[:3]
        context["seo"] = HomePageSeo.objects.first()
        return context
    
class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context["about"] = About.objects.first()
        context["partners"] = Partner.objects.all()
        context["seo"] = AboutPageSeo.objects.first()
        return context
    

class ShopPageView(ListView):
    template_name = 'shop.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        category_slug = self.request.GET.get('category')
        vendor_slug = self.request.GET.get('vendor')
        ordering = self.request.GET.get('ordering')
        search_query = self.request.GET.get('search')

        queryset = Product.objects.all().order_by('-stock', "pk")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if ordering:
            queryset = queryset.order_by('-stock', ordering)

        if vendor_slug:
            queryset = queryset.filter(vendor__slug=vendor_slug)

        return queryset
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('show', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category_slug = self.request.GET.get('category')
        vendor_slug = self.request.GET.get('vendor')
        ordering = self.request.GET.get('ordering')
        search_query = self.request.GET.get('search')

        queryset = Product.objects.all()

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if ordering:
            queryset = queryset.order_by(ordering)

        if vendor_slug:
            queryset = queryset.filter(vendor__slug=vendor_slug)

        context["count"] = queryset.count()
        context["categories"] = ProductCategory.objects.all()
        context["new_products"] = Product.objects.all().order_by("-id")[:3]
        context["companies"] = Company.objects.filter(finish_time__gte=datetime.datetime.now())[:4]
        context["seo"] = ShopPageSeo.objects.first()
        context["about"] = About.objects.first()

        return context

class ProductDetailPageView(DetailView):
    template_name = 'product-detail.html'
    model = Product
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailPageView, self).get_context_data(**kwargs)
        context["related_products"] = Product.objects.exclude(pk = self.get_object().pk).filter(category = self.get_object().category).order_by("-pk")[:4]
        return context
    

class BasketPageView(TemplateView, IsNotAuthView):
    template_name = 'basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_items = BasketItem.objects.filter(user=self.request.user).order_by("pk")
        
        all_items_in_stock = all(item.product.stock >= item.quantity for item in basket_items)
        context["items"] = basket_items
        context["all_items_in_stock"] = all_items_in_stock
        
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
        language = get_language()
        print(language)
        # Kullanıcıya ait sepet öğelerini al
        basket_items = BasketItem.objects.filter(user=request.user).order_by("pk")
        
        coupon_code = request.GET.get('coupon_code', None)
        
        # Sepet içeriğini JSON formatında döndür
        basket_items_data = [{
            'id': item.id,
            'product': {
                'id': item.product.pk,
                'title': getattr(item.product, f'title_{language}'),
                'slug': item.product.slug,
                'price': round_to_decimal(item.product.discount_price) if item.product.discount and item.product.stock > 0 else round_to_decimal(item.product.price),
                'image_url': item.product.image.url,
                'stock': item.product.stock,
                'url': item.product.get_absolute_url()
            },
            'quantity': item.quantity,
            'total_price': round_to_decimal(item.total_price),
        } for item in basket_items]
        
        basket_total = sum(item.total_price for item in basket_items)

    
        response_data = {
            'basketItemCount': basket_items.count(),
            'basketItems': basket_items_data,
            'totalPrice': round_to_decimal(basket_total),
            'stock_status': all(item.product.stock >= item.quantity for item in basket_items)
        }
        applied_coupon = None

        if coupon_code:
            try:
                applied_coupon = Coupon.objects.get(coupon=coupon_code)
                # Kuponun kullanılabilir olup olmadığını kontrol et
            except Coupon.DoesNotExist:
                response_data['error'] = _('Kupon mövcud deyil!')
                return JsonResponse(response_data)
        if applied_coupon:
            discounted_total = apply_coupon(request.user ,basket_items, applied_coupon)
            response_data["discountPrice"] = round_to_decimal(discounted_total)
            response_data["discount"] = round_to_decimal(basket_total - discounted_total),

        return JsonResponse(response_data)

    except Exception as e:
        response_data['error'] = _('Siz artıq bu kuponu istifadə etmisiz!')
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


from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    tracking_url = request.data.get("tracking_url")
    tracking_id = request.data.get("tracking_id")
    wolt_order_reference_id = request.data.get("wolt_order_reference_id")
        
    errors = []

    if not tracking_url:
        errors.append("Tracking URL is missing.")
    if not tracking_id:
        errors.append("Tracking ID is missing.")
    if not wolt_order_reference_id:
        errors.append("Wolt order reference ID is missing.")

    if errors:
        return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)
    parsed_url = urlparse(tracking_url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return Response({'error': "Tracking url doesn't exists."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        basket_items = BasketItem.objects.filter(user=request.user)

        if basket_items.count() == 0:
            return Response({'error': 'Səbətdə məhsul yoxdur!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Stok kontrolü
        for item in basket_items:
            product = Product.objects.get(id=item.product.id)
            if item.quantity > product.stock:
                return Response({'error': f"Stokda '{product.title}' yoxdur."}, status=status.HTTP_400_BAD_REQUEST)

        # Toplam ücret hesapla
        total_amount = sum(item.total_price for item in basket_items)

        # Kupon işlemleri
        coupon_code = request.data.get('coupon_code')
        applied_coupon = None

        if coupon_code:
            try:
                applied_coupon = Coupon.objects.get(coupon=coupon_code)
                # Kuponun kullanılabilir olup olmadığını kontrol et
                if not applied_coupon.can_user_use_coupon(request.user):
                    return Response({'error': 'Siz artıq bu kuponu istifadə etmisiz!'}, status=status.HTTP_400_BAD_REQUEST)
              
            except Coupon.DoesNotExist:
                return Response({'error': 'Kupon mövcud deyil!'}, status=status.HTTP_400_BAD_REQUEST)

        # İndirimli toplam tutarı hesapla

        # Sipariş oluştur

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,  # İndirimli toplam tutarı kullan
                discount=total_amount - apply_coupon(request.user, basket_items, applied_coupon) if applied_coupon else None,
                discount_amount=apply_coupon(request.user, basket_items, applied_coupon) if applied_coupon else None,
                coupon=applied_coupon,
                tracking_url = tracking_url,
                tracking_id = tracking_id,
                wolt_order_reference_id = wolt_order_reference_id
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
            coupon_usage = CouponUsage.objects.get(user=request.user, coupon=applied_coupon)
            coupon_usage.max_coupon_usage_count -= 1
            coupon_usage.save()
        return Response({'success': 'Sifarişiniz uğurla qeydə alındı.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': 'Sifariş oluşturulurken bir hata oluştu.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_stock_api(request):
    """
    Sepetteki ürünlerin stok durumunu kontrol eden REST API fonksiyonu.
    """
    try:
        basket_items = BasketItem.objects.filter(user=request.user)
        # Stok kontrolü
        errors = []
        for basket_item in basket_items:
            if basket_item.quantity > basket_item.product.stock:
                errors.append({'error': f"Stokda '{basket_item.product.title}' yoxdur."})

        if errors:
            return Response({'status': False, 'message': errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': True, 'message': 'Tüm ürünler stokta mevcut.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': 'Stok kontrolü yapılırken bir hata oluştu.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        context["seo"] = BlogPageSeo.objects.first()
        context["about"] = About.objects.first()
        return context
    
class BlogDetailPageView(DetailView):
    template_name = 'blog-detail.html'
    model = Blog
    context_object_name = "blog"
    
    def get_context_data(self, **kwargs):
        context = super(BlogDetailPageView, self).get_context_data(**kwargs)
        context["last_blogs"] = Blog.objects.exclude(pk = self.get_object().pk).order_by("-created")[:3]
        return context
    
class VacanciesPageView(TemplateView):
    template_name = 'vacancies.html'
    # paginate_by = 8
    # # model = News
    # context_object_name = 'vacancies'

    # def get_context_data(self, **kwargs):
    #     context = super(NewsPageView, self).get_context_data(**kwargs)
    #     context["last_news"] = News.objects.all()[:3]
    #     return context
    
    
class CompanyPageView(TemplateView):
    template_name = 'campanies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.filter(finish_time__gte=datetime.datetime.now())
        context["seo"] = CompaniesPageSeo.objects.first()
        context["about"] = About.objects.first()
        return context
    
class ContactPageView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        name = form.cleaned_data['name']
        number = form.cleaned_data['number']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        text = form.cleaned_data['text']
        
        data = {
            'name': name,
            'number' : number,
            'email': email,
            'subject': subject,
            'text': text,

        }
       
        message = render_to_string('mail/contact.html', data)

        send_mail(
            "Ecoproduct.az, müştəridən müraciət gəlib",
            message,
            settings.EMAIL_HOST_USER,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False, html_message=message
        )   
        messages.success(self.request, 'Mesajınız göndərildi!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = ContactPage.objects.first()
        context["seo"] = ContactPageSeo.objects.first()
        context["about"] = About.objects.first()

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

from django.http import HttpResponse
from .tasks import remove_expired_discounts

def start_task(request):
    task = remove_expired_discounts.delay(11)  # 10 saniyelik bir task başlatır
    return JsonResponse({'task_id': task.id})