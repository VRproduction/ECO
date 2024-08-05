from django.db import models
from django.core.exceptions import ValidationError

from apps.core.models import Supporter

class APIKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    is_external = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  
    supporter = models.ForeignKey(Supporter, on_delete = models.SET_NULL, related_name = 'api_keys', blank=True, null=True, verbose_name = "Dəstəkçi (Məsələn: Logix, ...)")  
    is_test = models.BooleanField(default = True)

    def clean(self):
        if self.is_external and not self.supporter or not self.is_external and  self.supporter:
            raise ValidationError('External API keys must have a supporter name.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.supporter.name if self.supporter else f"{self.key}"