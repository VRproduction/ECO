from django.contrib import admin
from .models import *

@admin.register(HomePageSeo)
class HomePageSeoAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
@admin.register(AboutPageSeo)
class AboutPageSeoAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
@admin.register(ShopPageSeo)
class ShopPageSeoAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
@admin.register(CompaniesPageSeo)
class CompaniesPageSeoAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
@admin.register(ContactPageSeo)
class ContactPageSeoAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
@admin.register(BlogPageSeo)
class BlogPageSeoAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)