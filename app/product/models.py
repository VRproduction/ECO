from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.utils import timezone

class IndexSlider(models.Model):
    title = models.CharField(max_length = 500)
    description = models.CharField(max_length = 500)
    image = models.ImageField(upload_to = 'index_slider')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Slayder'
        verbose_name_plural = 'Ana səhifə | Slayder'



class ProductCategory(models.Model):
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = 'category')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Kateqoriya'
        verbose_name_plural = 'Kateqoriyalar'

class Vendor(models.Model):
    title = models.CharField(max_length = 200)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendorlar'

class Product(models.Model):
    NUMBERS = [
        (1, "Ən çox satılan"),
        (2, "Yeni"),
        (3, "Endirim"),
        (4, "4-cü"),
    ]
    title = models.CharField(max_length = 500)
    category = models.ForeignKey(ProductCategory, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'products')
    badges = models.FloatField(choices = NUMBERS, blank = True, null = True)
    image = models.ImageField(upload_to = 'product')
    vendor = models.ForeignKey(Vendor, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'products')
    price = models.FloatField()
    discount = models.FloatField(null = True, blank = True)

    def __str__(self):
        return self.title
    
    @property
    def discount_price(self):
        return self.price*(100-self.discount)/100

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'

class CategoryBanner(models.Model):
    title = models.CharField(max_length = 500)
    category = models.OneToOneField(ProductCategory, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'banners')
    image = models.ImageField(upload_to = 'category_banner')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Ana səhifə | Seçilmiş Kategoriyalar | Banner'

class About(models.Model):
    title = models.CharField(max_length = 500)
    description = RichTextUploadingField(null = True, blank = True)
    image = models.ImageField(upload_to = 'about', verbose_name = "image(585x666)px")

    def __str__(self):
        return "Haqqımızda"
    
    class Meta:
        verbose_name = 'Haqqımızda'
        verbose_name_plural = 'Haqqımızda'

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
    is_active = models.BooleanField(default = True)

    def clean(self):
        super().clean()

        if self.finish_time and self.finish_time <= timezone.now():
            raise ValidationError({'finish_time': 'Finish time must be in the future.'})


    def __str__(self) -> str:
        return f'{self.product}'
    
    class Meta:
        verbose_name = 'Kompaniya'
        verbose_name_plural = 'Kompaniyalar'

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
    title = models.CharField(max_length = 500)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to = 'blogs', verbose_name = "photo(370x290)")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    is_main_page  = models.BooleanField(default = False, verbose_name = "Əsas səhifədə görünsün?")

    def __str__(self):
        return ('%s') % (self.title)

    class Meta:
        verbose_name = "Bloglar"
        verbose_name_plural = "Bloglar"

    # def get_absolute_url(self):
    #     return reverse("blog-detail", args=[str(self.pk)])