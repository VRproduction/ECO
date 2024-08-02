from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GeneralSettings(models.Model):
    site_title = models.CharField(
        max_length=200, verbose_name="Saytın başlığı")
    adress = models.CharField(max_length=1500, verbose_name="Ünvan", null=True, blank=True)
    email = models.EmailField(blank = True)
    g_adress = models.CharField(
        max_length=1500, verbose_name="Google Map linki", null=True, blank=True)
    g_adress_iframe = models.TextField(
        verbose_name="Google Map Iframe linki", null=True, blank=True)
    
    logo = models.FileField(verbose_name="logo(171x38)",
                            blank=True, upload_to="general_settings_logo")
    mobile_logo = models.FileField(verbose_name="Mobile logo(172x38)",
                                   help_text="Mobile logo", blank=True, null=True, upload_to="general_settings_mobile_logo")
    favicon = models.FileField(verbose_name="favicon(100x100)",
                               blank=True, null=True, upload_to="general_settings_favicon")
    footer_logo = models.FileField(help_text="Footer logo", blank=True, null=True, upload_to="general_settings_footer_logo")
    footer_slogan = models.TextField(null = True, blank = True)
    copyright_title = models.CharField(max_length = 100, blank = True)
    copyright_link = models.TextField(null = True, blank = True)
    facebook = models.CharField(
        max_length=200, verbose_name="Facebook", blank=True)
    instagram = models.CharField(
        max_length=200, verbose_name="Instagram", blank=True)
    youtube = models.CharField(
        max_length=200, verbose_name="Youtube", blank=True)
    tiktok = models.CharField(
        max_length=200, verbose_name="TikTok", blank=True)
    work_start_hour = models.TimeField(verbose_name="İşin başlama saatı", null = True)
    work_finish_hour = models.TimeField(verbose_name="İşin bitmə saatı", null = True)
    
    def __str__(self):
        return ('%s') % (self.site_title)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "General Settings"

class PhoneNumber(models.Model):
    number = models.CharField(max_length=200, blank=True, null = True)
    setting = models.ForeignKey(GeneralSettings, on_delete = models.CASCADE, related_name = 'numbers', null = True, blank = True)
    is_main = models.BooleanField(default = False)

    def __str__(self):
        return ('%s') % (self.number)

    class Meta:
        verbose_name = "Nömrə"
        verbose_name_plural = "Nömrələr"