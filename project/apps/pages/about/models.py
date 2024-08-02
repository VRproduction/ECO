from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

class About(models.Model):
    title = models.CharField(max_length = 500)
    description = RichTextUploadingField(null = True, blank = True)
    image = models.ImageField(upload_to = 'about', verbose_name = "image(585x666)px")

    def __str__(self):
        return "Haqqımızda"
    
    class Meta:
        verbose_name = 'Haqqımızda'
        verbose_name_plural = 'Haqqımızda'