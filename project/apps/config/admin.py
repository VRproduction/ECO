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
    
class WeekDayAdmin(admin.ModelAdmin):
    list_display = ('get_day_of_week_display', 'is_workday', 'work_start_hour', 'work_finish_hour')
    list_filter = ('is_workday',)
    ordering = ('day_of_week',)
    search_fields = ('get_day_of_week_display',)
    
    def get_day_of_week_display(self, obj):
        return obj.get_day_of_week_display()
    get_day_of_week_display.short_description = 'Day of the Week'

admin.site.register(WeekDay, WeekDayAdmin)

# admin.py
from django.contrib import admin
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'supporter', 'is_external', 'is_active', 'is_test')
    search_fields = ('key', 'supporter')
    list_filter = ('supporter', "is_test")
    
@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('url', 'ip_address', 'timestamp', 'user')
    list_filter = ('timestamp', 'url')
    search_fields = ('url', 'ip_address', 'user')

@admin.register(MonitoredURL)
class MonitoredURLAdmin(admin.ModelAdmin):
    list_display = ('url_pattern', 'is_monitored')
    list_filter = ('is_monitored',)
    search_fields = ('url_pattern',)