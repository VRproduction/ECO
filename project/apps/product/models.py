from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.payment.models import Transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.config.models.api_key import APIKey
from apps.core.models import Supporter

from utils.slugify.custom_slugify import custom_az_slugify
from utils.models.clickable_model import ClickableModel

User = get_user_model()

class ProductCategory(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to = 'category')
    is_main_page = models.BooleanField(default = True)

    created_by_supporter = models.ForeignKey(Supporter, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'product_categories', verbose_name = 'Dəstəkçi')
    is_active = models.BooleanField(default = True, verbose_name = "Saytda görünən və ya aktiv olan", help_text="Supporter (Məsələn: logix) tərəfindan yaradıldığı zaman təsdiqlənmədən aktiv olmasına icazə verilmir.")    
    is_test = models.BooleanField(default = False, verbose_name = "Test üçün (Saytda görünmür)")  

    created = models.DateTimeField(auto_now_add = True, null = True)
    updated = models.DateTimeField(auto_now = True, null = True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Kateqoriya'
        verbose_name_plural = 'Kateqoriyalar'

    def clean(self):
        super().clean()

        if self.is_active and not self.image:
            raise ValidationError("Kateqoriyanın aktiv olması üçün şəkil yükləmək tələb olunur.")
        
        if self.is_active and self.is_test:
            raise ValidationError("Test və saytda görünən eyni zamanda aktiv ola bilməz. ")
        

    def save(self, *args, **kwargs):
        self.slug = custom_az_slugify(self.title)
        super(ProductCategory, self).save(*args, **kwargs)

class Vendor(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(blank=True, null=True, unique = True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendorlar'

    def save(self, *args, **kwargs):
        self.slug = custom_az_slugify(self.title)
        super(Vendor, self).save(*args, **kwargs)

class Coupon(models.Model):
    coupon = models.CharField(max_length=50)
    discount_percent = models.FloatField(null=True, blank=True) 
    discount_amount = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return self.coupon
    
    def apply_discount(self,user, basket_total):
        # Kullanım kontrolü ekleniyor
        if not self.can_user_use_coupon(user):
            raise ValidationError('Siz artıq bu kuponu istifadə etmisiz!')

        if self.discount_percent:
            return basket_total * (100 - self.discount_percent) / 100
        elif self.discount_amount:
            return max(basket_total - self.discount_amount, 0)
        else:
            return basket_total
        
    def can_user_use_coupon(self, user):
        used_count = CouponUsage.objects.filter(user=user, coupon=self).first().max_coupon_usage_count
        return used_count > 0
        
    class Meta:
        verbose_name = 'Kupon'
        verbose_name_plural = 'Kuponlar'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create CouponUsage for all users
        users = User.objects.all()
        for user in users:
            CouponUsage.objects.get_or_create(user=user, coupon=self, defaults={'max_coupon_usage_count': 1})



class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'coupon_usages')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name = 'coupon_usages')
    max_coupon_usage_count = models.PositiveIntegerField(default=1)
    used_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'coupon']
        verbose_name = 'Kupon'
        verbose_name_plural = 'İstifadə edilən kuponlar'
    
    def __str__(self):
        return f"{self.coupon}"
    
class Product(ClickableModel):
    NUMBERS = [
        (1, _("Ən çox satılan")),
        (2, _("Yeni")),
        (3, _("Endirim")),
        (4, _("4-cü")),
    ]
    title = models.CharField(max_length = 500)
    slug = models.SlugField(blank=True, null=True, unique = True, max_length = 255)
    description = RichTextUploadingField(null = True, blank = True)
    using_time = models.PositiveIntegerField(null = True, blank = True, verbose_name = "İstifadə müddəti")
    category = models.ForeignKey(ProductCategory, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'products')
    badges = models.IntegerField(choices = NUMBERS, blank = True, null = True)
    image = models.ImageField(upload_to = 'product', blank = True, null = True)
    vendor = models.ForeignKey(Vendor, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'products')
    price = models.FloatField()
    discount = models.PositiveIntegerField(null = True, blank = True)
    stock = models.PositiveIntegerField(default=0)
    sale_count = models.PositiveIntegerField(default=0, null = True, verbose_name = "Satış sayı")
    
    is_active = models.BooleanField(default = True, verbose_name = "Saytda görünən və ya aktiv olan", help_text="Supporter (Məsələn: logix) tərəfindan yaradıldığı zaman təsdiqlənmədən aktiv olmasına icazə verilmir.")    
    is_test = models.BooleanField(default = False, verbose_name = "Test üçün (Saytda görünmür)")    
    
    is_main_page = models.BooleanField(default = False, verbose_name = "Ana səhifədə görünən")
    is_best_seller = models.BooleanField(default = False, verbose_name = "Ən çox satılan")
    is_most_wonted = models.BooleanField(default = False, verbose_name = "Ən çox axtarılan")
    is_trending = models.BooleanField(default = False, verbose_name = "Trenddə olan")
    
    barcode_code = models.BigIntegerField('Məhsulun barkodu', default=0)
    product_code = models.IntegerField('Məhsulun kodu', null=True, blank=True)

    created_by_supporter = models.ForeignKey(Supporter, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'products', verbose_name = 'Dəstəkçi')

    keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    logix_product_id = models.PositiveBigIntegerField(null = True, blank = True)

    created = models.DateTimeField(auto_now_add = True, null = True)
    updated = models.DateTimeField(auto_now = True, null = True)

    def __str__(self):
        return self.title
    
    @property
    def discount_price(self):
        return self.price*(100-self.discount)/100
    
    @property
    def sitemap_image(self):
        return self.image.url if self.image else None
    

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'
        ordering = ['-stock', '-pk']
    
    def clean(self):
        super().clean()
        
        if self.title:
            product = Product.objects.filter(title=self.title).exists()
            if product:
                raise ValidationError("Bu adlı məhsul artıq movcuddur.")

        if self.is_best_seller:
            best_sellers_count = Product.objects.filter(is_best_seller=True).count()
            if best_sellers_count >= 3 and not Product.objects.filter(is_best_seller=True, pk = self.pk).exists():
                raise ValidationError("Ən çox 3 'Ən çox satılan' ola bilər.")

        if self.is_most_wonted:
            most_wonted_count = Product.objects.filter(is_most_wonted=True).count()
            if most_wonted_count >= 3 and not Product.objects.filter(is_most_wonted=True, pk = self.pk).exists():
                raise ValidationError("Ən çox 3 'Ən çox axtarılan' ola bilər.")

        if self.is_trending:
            trending_count = Product.objects.filter(is_trending=True).count()
            if trending_count >= 3 and not Product.objects.filter(is_trending=True, pk = self.pk).exists():
                raise ValidationError("Ən çox 3 'Trenddə olan' ola bilər.")
            
        if self.is_active and not self.image:
            raise ValidationError("Məhsulun aktiv olması üçün şəkil yükləmək tələb olunur.")
        
        if self.is_active and self.is_test:
            raise ValidationError("Test və saytda görünən eyni zamanda aktiv ola bilməz. ")
        
        
    def save(self, *args, **kwargs):
        self.slug = custom_az_slugify(self.title)
        if self.barcode_code:
            barcode_str = str(self.barcode_code)
            self.product_code = int(barcode_str[-4:])
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product-detail", args=[str(self.slug)])
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True, blank = True, related_name = 'images')
    image = models.ImageField(upload_to = 'product')

    def __str__(self):
        return f'{self.product} | {self.pk}'
    
    class Meta:
        verbose_name = 'Şəkil'
        verbose_name_plural = 'Şəkillər'

class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'favorites')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'favorites')

    def __str__(self):
        return f'{self.user.email} | {self.product}'

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Sevimlilər'


class BasketItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'basket_items', null = True, blank = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'basket_items', null = True, blank = True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * (self.product.discount_price) if self.product.discount else (self.quantity * self.product.price)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title} for {self.user.email}"

    def to_dict_for_wolt_delivery(self):
        return {
            "price": {
                "amount": round(self.total_price, 2),
                "currency": "AZN"  # Replace with your actual currency
            },
            "description": self.product.title,
            "count": self.quantity
        }

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Səbətdəki məhsullar'

class Order(models.Model):

    TYPE_CHOICES = (
        ('Yeni', 'Yeni'),
        ('Paketlənən', 'Paketlənən'),
        ('Təhvilə hazır', 'Təhvilə hazır'),
        ('Tamamlanmış', 'Tamamlanmış'),
        ('Ləğv edilib', 'Ləğv edilib')
    )

    BOX_CHOICES = [
        ('Kiçik', 'Kiçik'),
        ('Orta', 'Orta'),
        ('Böyük', 'Böyük')
    ]
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'orders', null = True, blank = True)
    total_amount = models.FloatField()
    discount = models.FloatField(null = True, blank = True)
    discount_amount = models.FloatField(null = True, blank = True)
    delivery_amount = models.FloatField(null = True, blank = True)
    is_delivery_free = models.BooleanField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete = models.CASCADE, related_name = 'orders', null = True, blank = True)
    tracking_url = models.URLField(null = True, blank = True)
    tracking_id = models.CharField(max_length = 100, null = True, blank = True)
    wolt_order_reference_id = models.CharField(max_length = 100, null = True, blank = True)
    is_wolt = models.BooleanField(default = False)
    transaction = models.OneToOneField(Transaction, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'order')
    order_type =  models.CharField('Sifariş növü', max_length=20, choices=TYPE_CHOICES, default='Yeni')
    box_choice = models.CharField('Qutu seçimi', choices=BOX_CHOICES, max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user} | {self.pk}"

    class Meta:
        verbose_name = 'Sifariş'
        verbose_name_plural = 'Sifarişlər'
        ordering = ['-created_at']

    def get_confirmed_statuses(self):
        return self.statuses.filter(is_confirmed=True)
    
    @property
    def confirmed_status(self):
        confirmed_status_obj = self.statuses.filter(is_confirmed=True).order_by('-ordering').first()
        if confirmed_status_obj:
            return confirmed_status_obj.status
        return None
    
class Status(models.Model):
    status = models.CharField(max_length=20, choices=[
        ('Gözləmədə', _('Gözləmədə')),
        ('Hazırlandı', _('Hazırlandı')),
        ('Göndərilib', _('Göndərilib')),
        ('Çatdırılıb', _('Çatdırılıb')),
        ('Ləğv edilib', _('Ləğv edilib')),
    ], default='Gözləmədə')
    is_confirmed = models.BooleanField(default=False, verbose_name="Təsdiqlənib")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='statuses')
    ordering = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk: 
            highest_ordering = Status.objects.filter(order=self.order).aggregate(models.Max('ordering'))['ordering__max']
            if highest_ordering is not None:
                self.ordering = highest_ordering + 1

                
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        existing_instance = Status.objects.get(pk=self.pk)
        if not self.is_confirmed and self.pk and existing_instance.is_confirmed:
            raise ValidationError("Artıq status təsdiqlənib!")
            

    def __str__(self):
        return f"{self.status}"

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuslar'
        ordering = ['order', 'ordering']
        unique_together = (('status', 'order'),)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name = 'order_items', null = True, blank = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'order_items', null = True, blank = True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order {self.order.id}"
    
    @property
    def total_price(self):
        return self.quantity * (self.product.discount_price) if self.product.discount else (self.product.price)
    
    def to_dict_for_wolt_delivery(self):
        return {
            "price": {
                "amount": round(self.total_price, 2),
                "currency": "AZN"  # Replace with your actual currency
            },
            "description": self.product.title,
            "count": self.quantity
        }
    
    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'


class Feature(models.Model):
    title1 = models.CharField(max_length = 200)
    title2 = models.CharField(max_length = 200)
    icon = models.FileField(upload_to = 'featured', null = True, blank = True)

    def __str__(self):
        return self.title1
    
    class Meta:
        verbose_name = 'Özəllik'
        verbose_name_plural = 'Özəlliklər'
    
class Company(models.Model):
    image = models.ImageField(upload_to = 'company', verbose_name = "image(379x335)px", null = True)
    product = models.OneToOneField(Product, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'company')
    discount = models.FloatField(null = True, blank = True)
    finish_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add = True)

    def clean(self):
        super().clean()

        if self.finish_time and self.finish_time <= timezone.now():
            raise ValidationError({'finish_time': 'Finish time must be in the future.'})


    def __str__(self) -> str:
        return f'{self.product}'
    
    class Meta:
        verbose_name = 'Kompaniya'
        verbose_name_plural = 'Kompaniyalar'

    def schedule_discount_removal(self):
        from .tasks import remove_expired_discounts
        eta = self.finish_time - timezone.now()
        if eta.total_seconds() > 0:
            remove_expired_discounts.apply_async(
                (self.id,),
                eta=self.finish_time
            )

class Partner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to = "partners")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Tərəfdaş'
        verbose_name_plural = 'Tərəfdaşlar'

class Statistic(models.Model):
    year = models.IntegerField(blank = True, null = True)
    product = models.BigIntegerField(blank = True, null = True)
    category = models.IntegerField(blank = True, null = True)
    brend = models.IntegerField(blank = True, null = True)
    new_taste = models.IntegerField(blank = True, null = True)
    image = models.ImageField(upload_to = 'statistic', verbose_name = "img(610x315)", blank = True, null = True)

    def __str__(self):
        return 'Statistika'
    
    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistika'

class FAQ(models.Model):
    title = models.CharField(max_length = 500)
    description = models.TextField()

    def __str__(self):
        return ('%s') % (self.title)

    class Meta:
        verbose_name = "Sual"
        verbose_name_plural = "Suallar"

class Blog(models.Model):
    title = models.CharField(max_length = 500, unique = True)
    slug = models.SlugField(blank=True, null=True, unique = True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to = 'blogs', verbose_name = "photo(370x290)")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    is_main_page  = models.BooleanField(default = False, verbose_name = "Əsas səhifədə görünsün?")
 
    keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    @property
    def sitemap_image(self):
        return self.image.url if self.image else None

    def __str__(self):
        return ('%s') % (self.title)

    class Meta:
        verbose_name = "Bloglar"
        verbose_name_plural = "Bloglar"
        ordering = ['-pk']

    def get_absolute_url(self):
        return reverse("blog-detail", args=[str(self.slug)])
    
    def save(self, *args, **kwargs):
        self.slug = custom_az_slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

class Contact(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField()
    number = models.CharField(max_length = 50)
    subject = models.CharField(max_length = 200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return ('%s') % (self.name)

    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"

class ContactPage(models.Model):
    image = models.ImageField(upload_to = 'contact_page')

    def __str__(self):
        return "Əlaqə səhifəsi"

    class Meta:
        verbose_name = "Əlaqə səhifəsi"
        verbose_name_plural = "Əlaqə səhifəsi"