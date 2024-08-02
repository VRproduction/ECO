from django.db import models
from apps.product.models import ProductCategory

class IndexSlider(models.Model):
    title = models.CharField(max_length = 500)
    mobile_title = models.CharField(max_length = 500, null = True)
    description = models.CharField(max_length = 500)
    mobile_description = models.CharField(max_length = 500, null = True)
    image = models.ImageField(upload_to = 'index_slider')
    mobile_image = models.ImageField(upload_to = 'index_slider_mobile',verbose_name = 'Mobile photo(366x350px)', null = True, blank = True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Slayder'
        verbose_name_plural = 'Slayder'


class CategoryBanner(models.Model):
    title = models.CharField(max_length = 500)
    category = models.OneToOneField(ProductCategory, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'banners')
    image = models.ImageField(upload_to = 'category_banner')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Seçilmiş Kategoriyalar | Banner'
