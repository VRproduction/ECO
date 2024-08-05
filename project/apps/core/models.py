from django.db import models

class Supporter(models.Model):
    name = models.CharField(unique = True, max_length=255, blank=True, null=True, verbose_name = "Dəstəkçi (Məsələn: Logix, ...)")  

    def __str__(self) -> str:
        return self.name