from django.contrib import admin
from .models import *

MAX_OBJECTS = 1


@admin.register(Wolt)
class WoltAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'value', 'is_wolt', 'order', 'created']