from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth import get_backends

User = get_user_model()

MAX_OBJECTS = 1

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber

@admin.register(GeneralSettings)
class SettingAdmin(admin.ModelAdmin):
    inlines = [PhoneNumberInline, ]
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    
@admin.register(IndexSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(ProductCategory)
admin.site.register(Vendor)

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    list_display = ('title', 'category','id', 'price', 'stock', 'sale_count', 'is_best_seller', 'is_most_wonted', 'is_trending',  'is_main_page')
    list_filter = ('category', 'is_main_page', 'is_best_seller', 'is_most_wonted', 'is_trending')
    search_fields = ('title', 'description')
    ordering = ('-stock',)
    readonly_fields = ('sale_count',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'slug')
        }),
        ('Product Information', {
            'fields': ('using_time', 'badges', 'image', 'vendor', 'price', 'discount', 'stock', 'sale_count')
        }),
        ('Special Markers', {
            'fields': ('is_main_page', 'is_best_seller', 'is_most_wonted', 'is_trending')
        }),
    )


@admin.register(CategoryBanner)
class CategoryBannerAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= 3:
            return False
        return super().has_add_permission(request)
    
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= 5:
            return False
        return super().has_add_permission(request)
    
admin.site.register(Company)
admin.site.register(Partner)

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    
admin.site.register(FAQ)
admin.site.register(Blog)
    
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
    readonly_fields = ['id', 'user', 'total_amount', 'created_at', 'coupon', 'discount', 'discount_amount', 'tracking_url', 'tracking_id', 'wolt_order_reference_id', 'is_wolt', 'transaction']
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