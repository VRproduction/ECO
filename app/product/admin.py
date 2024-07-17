from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth import get_backends
from modeltranslation.admin import TranslationAdmin

User = get_user_model()

MAX_OBJECTS = 1

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber

@admin.register(GeneralSettings)
class SettingAdmin(TranslationAdmin):
    inlines = [PhoneNumberInline, ]
    list_display = ('site_title',)
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
@admin.register(IndexSlider)
class HomePageSliderAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Vendor)
class VendorAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline, ]
    list_display = ('title', 'category','id', 'price', 'stock', 'sale_count', 'is_best_seller', 'is_most_wonted', 'is_trending',  'is_main_page')
    list_filter = ('category', 'is_main_page', 'is_best_seller', 'is_most_wonted', 'is_trending')
    search_fields = ('title', 'description')
    ordering = ('-stock',)
    readonly_fields = ('sale_count', 'product_code')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'slug')
        }),
        ('Product Information', {
            'fields': ('using_time', 'badges', 'image', 'vendor', 'price', 'discount', 'stock', 'sale_count', 'barcode_code', 'product_code')
        }),
        ('Special Markers', {
            'fields': ('is_main_page', 'is_best_seller', 'is_most_wonted', 'is_trending')
        }),
        ('SEO', {
            'fields': ('keywords', 'meta_description')
        }),
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(CategoryBanner)
class CategoryBannerAdmin(TranslationAdmin):
    list_display = ('title',)
    def has_add_permission(self, request):
        if self.model.objects.count() >= 3:
            return False
        return super().has_add_permission(request)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
@admin.register(About)
class AboutAdmin(TranslationAdmin):
    list_display = ('title',)

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
@admin.register(Feature)
class FeatureAdmin(TranslationAdmin):
    list_display = ('title1',)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 5:
            return False
        return super().has_add_permission(request)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
admin.site.register(Company)

@admin.register(Partner)
class PartnerAdmin(TranslationAdmin):
    list_display = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    
@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['order', 'quantity']

    def has_add_permission(self, request, obj=None):
        return False


class StatusInline(admin.TabularInline):
    model = Status
    extra = 0
    readonly_fields = ['status',]
    fields = ['status', 'is_confirmed',]

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False  

    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'confirmed_status', 'id','total_amount', 'is_wolt', 'created_at']
    list_filter = ['is_wolt',]
    search_fields = ['id','user__email']
    readonly_fields = [
        'id', 'user', 'total_amount', 'created_at', 
        'coupon', 'discount', 'discount_amount', 
        'tracking_url', 'tracking_id', 
        'wolt_order_reference_id', 'is_wolt', 
        'transaction', 'order_type', 'box_choice']
    inlines = [StatusInline, OrderItemInline, ]


admin.site.register(Favorite)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created']
    search_fields = ['email']
    readonly_fields = ['name', 'email','number', 'subject', 'text', 'created']

admin.site.register(BasketItem)
admin.site.register(ContactPage)


class CouponUsageInline(admin.TabularInline):
    model = CouponUsage

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    inlines = [CouponUsageInline, ]