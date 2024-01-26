from django.contrib import admin
from .models import *

MAX_OBJECTS = 1

@admin.register(IndexSlider)
class HomePageSliderAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= 2:
            return False
        return super().has_add_permission(request)
    
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Vendor)

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
    