from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from product.models import Product, Blog

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return [
            'home', 'about', 'shop',
            'companies', 'contact', 'blog',
        ]

    def location(self, item):
        return reverse(item)
    
class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Product.objects.all()
    
    def location(self, obj):
        return f'/products/{obj.slug}/'
    
class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Blog.objects.all()
    
    def lastmod(self, obj):
        return obj.updated
    
    def location(self, obj):
        return f'/blogs/{obj.slug}/'