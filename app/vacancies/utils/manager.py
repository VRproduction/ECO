from django.db import models

from vacancies import models as mod

class PublishedVacancyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.Vacancy.Status.PUBLİSHED)