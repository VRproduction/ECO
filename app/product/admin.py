from django.contrib import admin
from .models import *

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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = [OrderItemInline, ]
    
admin.site.register(BasketItem)
admin.site.register(Favorite)
admin.site.register(Contact)