from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib import messages  # Import messages
from django.utils.translation import gettext_lazy as _

User = get_user_model()

MAX_OBJECTS = 1

    
class ImageNullFilter(admin.SimpleListFilter):
    title = _('Şəkil olanlar')
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image__isnull=True).exclude(image__exact='')
        if self.value() == 'no':
            return queryset.filter(image__isnull=True) | queryset.filter(image__exact='')

    
@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ('title',  'is_active', 'is_test', 'is_main_page', "created")
    list_filter = (ImageNullFilter, 'is_active', 'is_test', 'created_by_supporter', 'is_main_page')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Varsayılan olarak sadece 'active=True' olanları göster
        if not request.GET.get('is_active__exact'):
            qs = qs.filter(is_active=True)
        return qs

@admin.register(Vendor)
class VendorAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline, ]
    list_display = ('title', 'category','id', 'price', 'stock', 'sale_count', 'click_count', 'is_active', 'is_test', 'is_best_seller', 'is_most_wonted', 'is_trending',  'is_main_page', "created")
    list_filter = (ImageNullFilter, 'is_active', 'is_test', 'created_by_supporter', 'category', 'is_main_page', 'is_best_seller', 'is_most_wonted', 'is_trending', )
    search_fields = ('title', 'description')
    ordering = ('-stock',)
    readonly_fields = ('sale_count', 'product_code', 'created', 'updated', 'click_count')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'slug', 'created_by_supporter')
        }),
        ('Product Information', {
            'fields': ('using_time', 'badges', 'image', 'vendor', 'price', 'discount', 'stock', 'sale_count', 'barcode_code', 'product_code')
        }),
        ('Special Markers', {
            'fields': ('is_active', 'is_test', 'is_main_page', 'is_best_seller', 'is_most_wonted', 'is_trending', 'click_count')
        }),
        ('SEO', {
            'fields': ('keywords', 'meta_description')
        }),
        ('Times', {
            'fields': ('created', 'updated')
        }),
    )
    # def get_click_count(self, obj):
    #     return obj.get_click_count()
    # get_click_count.short_description = 'Click Count'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Varsayılan olarak sadece 'active=True' olanları göster
        if not request.GET.get('is_active__exact'):
            qs = qs.filter(is_active=True)
        return qs

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    
@admin.register(Feature)
class FeatureAdmin(TranslationAdmin):
    list_display = ('title1',)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 5:
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
    
admin.site.register(Company)

@admin.register(Partner)
class PartnerAdmin(TranslationAdmin):
    list_display = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
    
@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # readonly_fields = ['order', 'quantity']

    # def has_add_permission(self, request, obj=None):
    #     return False


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
    # readonly_fields = [
    #     'id', 'user', 'total_amount', 'created_at', 
    #     'coupon', 'discount', 'discount_amount', 
    #     'tracking_url', 'tracking_id', 
    #     'wolt_order_reference_id', 'is_wolt', 
    #     'transaction', 'order_type', 'box_choice']
    inlines = [OrderItemInline, ]


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