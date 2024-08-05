from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


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
    
# admin.py
from django.contrib import admin
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'supporter_name', 'is_external', 'is_active', 'is_test')
    search_fields = ('key', 'supporter_name')
    list_filter = ('supporter_name', "is_test")
    