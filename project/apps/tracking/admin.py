from django.contrib import admin
from django.http import HttpRequest
from .models import ClickTracking, IPAddress

class IPAddressInline(admin.TabularInline):
    model = IPAddress
    extra = 0
    readonly_fields = ('ip_address','created', 'updated')

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request):
        return False
    
    def has_delete_permission(self, request):
        return False

class ClickTrackingAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'click_count')
    inlines = [IPAddressInline]
    readonly_fields = ('click_count', 'created', 'updated')

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request):
        return False
    
    def has_delete_permission(self, request):
        return False
    
admin.site.register(ClickTracking, ClickTrackingAdmin)

class IPAddressAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request):
        return False
    
    def has_delete_permission(self, request):
        return False
    
admin.site.register(IPAddress, IPAddressAdmin)
