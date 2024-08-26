from django.contrib import admin
from django.http import HttpRequest
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import *

from apps.product.models import BasketItem

MAX_OBJECTS = 1

@admin.register(LoginRegisterPage)
class HomePageSliderAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    

class BasketInline(admin.TabularInline):
    model = BasketItem
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False  
    def has_change_permission(self, request, obj=None):
        return False

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "is_superuser", "created", 'order_count', 'basket_items_count')
    list_filter = ("email", "is_staff", "is_active",)
    readonly_fields = ("created", "updated")
    fieldsets = (
        (None, {"fields": ("first_name", "last_name","email", "password", "created", "updated")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    inlines = [BasketInline, ]

   

    def order_count(self, obj):
        return obj.order_count   
    
    def basket_items_count(self, obj):
        return obj.basket_items_count   

    order_count.short_description = 'Sifariş sayı'
    basket_items_count.short_description = 'Səbətdə'

admin.site.register(CustomUser, CustomUserAdmin)


