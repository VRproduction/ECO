from django.db import models

class HomePageSeo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Home Page SEO'
        verbose_name_plural = 'Home Page SEO'

class AboutPageSeo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'About Page SEO'
        verbose_name_plural = 'About Page SEO'

class ShopPageSeo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Shop Page SEO'
        verbose_name_plural = 'Shop Page SEO'

class CompaniesPageSeo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Companies Page SEO'
        verbose_name_plural = 'Companies Page SEO'

class ContactPageSeo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Contact Page SEO'
        verbose_name_plural = 'Contact Page SEO'

class BlogPageSeo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog Page SEO'
        verbose_name_plural = 'Blog Page SEO'
