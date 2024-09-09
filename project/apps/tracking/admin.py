from django.contrib import admin
from .models import ClickTracking, IPAddress

class IPAddressInline(admin.TabularInline):
    model = IPAddress
    extra = 0
    readonly_fields = ('ip_address', 'created', 'updated')

    # Disable adding new inlines
    def has_add_permission(self, request, obj=None):
        return False

    # Disable deleting existing inlines
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    def has_change_permission(self, request, obj=None):
        return False

class ClickTrackingAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'click_count')
    read_only_fields = ('content_type', 'object_id', 'click_count')
    inlines = [IPAddressInline]
    
    # Make all fields read-only

    # Disable adding new objects
    def has_add_permission(self, request):
        return False

    # Disable deleting existing objects
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(ClickTracking, ClickTrackingAdmin)

class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'created', 'updated')
    read_only_fields = ('ip_address', 'created', 'updated')

    # Make all fields read-only

    # Disable adding new objects
    def has_add_permission(self, request):
        return False

    # Disable deleting existing objects
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(IPAddress, IPAddressAdmin)