from django.db import models
from django.core.exceptions import ValidationError

class APIKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    is_external = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  
    supporter_name = models.CharField(unique = True, max_length=255, blank=True, null=True, verbose_name = "Dəstəkçi (Məsələn: Logix, ...)")  
    is_test = models.BooleanField(default = True)

    def clean(self):
        if self.is_external and not self.supporter_name or not self.is_external and  self.supporter_name:
            raise ValidationError('External API keys must have a supporter name.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.supporter_name if self.supporter_name else f"{self.key}"