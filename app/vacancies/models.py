from typing import Collection, Iterable
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import (
    validate_email, 
    FileExtensionValidator
)

from ckeditor_uploader.fields import RichTextUploadingField

from product.utils.custom_slugify import custom_az_slugify
from vacancies.utils.manager import (
    PublishedVacancyManager
)

class Base(models.Model):

    class Status(models.TextChoices):
            DRAFT = 'DF', 'Draft'
            PUBLİSHED = 'PB', 'Published'

    created_at = models.DateTimeField(
        'Vakansiyanın əlavə edilmə tarixi', 
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Yenilənmə tarixi', 
        auto_now=True
    )
    published_at = models.DateTimeField(
        'Yayımlanma tarixi', 
        auto_now_add=True
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PUBLİSHED
    )

    class Meta:
        abstract = True

    @property
    def created_date(self):
        local_created_time = timezone.localtime(self.created_at)
        return local_created_time.strftime('%d %b %Y')
    
    @property
    def published_date(self):
        local_published_time = timezone.localtime(self.published_at)
        return local_published_time.strftime('%d %b %Y')
    

class IPs(models.Model):
    view_ip = models.GenericIPAddressField('IP ünvanı', editable=False)

    class Meta:
        verbose_name = ('IP ünvanı')
        verbose_name_plural = ('IP ünvanları')

    def __str__(self) -> str:
        return self.view_ip
    

class CompanyDepartment(models.Model):
    department_name = models.CharField('Şöbənin adı', max_length=200, unique=True)
    slug=models.SlugField(
        'Link adı',
        null=True, blank=True,
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        max_length=500    
    )

    class Meta:
        verbose_name = 'Şöbə'
        verbose_name_plural = 'Şöbələr'

    def __str__(self) -> str:
        return self.department_name
    
    def save(self) -> None:
        if not self.slug:
            self.slug = custom_az_slugify(self.department_name)
        return super().save()
    

class WorkingHour(models.Model):
    work_hour = models.CharField('İş qrafiki', max_length=200, unique=True)
    slug=models.SlugField(
        'Link adı',
        null=True, blank=True,
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        max_length=500    
    )

    class Meta:
        verbose_name = 'İş qrafiki'
        verbose_name_plural = 'İş qrafikləri'

    def __str__(self) -> str:
        return self.work_hour
    
    def save(self) -> None:
        if not self.slug:
            self.slug = custom_az_slugify(self.work_hour)
        return super().save()
    

class VacancyType(models.Model):
    vacancy_type = models.CharField('Elanın növü', max_length=200, unique=True)
    slug=models.SlugField(
        'Link adı',
        null=True, blank=True,
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        max_length=500    
    )

    class Meta:
        verbose_name = 'Elanın növü'
        verbose_name_plural = 'Elanın növləri'

    def __str__(self) -> str:
        return self.vacancy_type
    
    def save(self) -> None:
        if not self.slug:
            self.slug = custom_az_slugify(self.vacancy_type)
        return super().save()
    

class Vacancy(Base):
    vacancy_title = models.CharField('Vakant yerin adı', max_length=200)
    vacancy_content = RichTextUploadingField(
        'Vakansiyanın təsviri'
    )
    salary = models.IntegerField(
        'Əmək haqqı', 
        help_text='Məbləği manatla daxil edin.',
        default='345',
    )
    deadline = models.DateTimeField(
        'Son müraciət tarixi', 
        default=timezone.now
    )
    vacancy_type = models.ForeignKey(
        VacancyType,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Elanın növü',
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        CompanyDepartment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Şöbə',
        related_name='vacancies'
    )
    work_hour = models.ForeignKey(
        WorkingHour,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='İş qrafiki',
        null=True,
        blank=True
    )
    viewed_ips = models.ManyToManyField(
        IPs, 
        related_name="vacancies", 
        verbose_name='Elanın görüntüləndiyi IP ünvanları', 
        editable=False
    )
    slug=models.SlugField(
        'Link adı',
        null=True, blank=True,
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        max_length=500    
    )
    objects = models.Manager()
    published = PublishedVacancyManager()

    class Meta:
        verbose_name = 'Vakansiya'
        verbose_name_plural = 'Vakansiyalar'
        ordering = ('-published_at', '-updated_at')
        indexes = [
            models.Index(fields=('-published_at', '-updated_at'))
        ]

    def __str__(self) -> str:
        return self.vacancy_title
    
    @property
    def view_count(self):
        return self.viewed_ips.count() if self.viewed_ips else 0
    
    @property
    def application_count(self):
        return self.applications.count() if self.applications else 0
    
    @property
    def deadline_date(self):
        local_deadline = timezone.localtime(self.deadline)
        return local_deadline.strftime('%d %b %Y, %H:%M')
    
    def get_absolute_url(self):
        return reverse('vacancy-detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        status = self.status
        if status != self.Status.PUBLİSHED:
            self.published_at = timezone.now()
        if not self.slug:
            self.slug = custom_az_slugify(self.vacancy_title)
        super().save(*args, **kwargs)
    

class VacancyApplication(models.Model):
    created_at = models.DateTimeField(
        'Müraciətin edilmə tarixi', 
        auto_now_add=True
    )
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Elan'
    )
    full_name = models.CharField(
        'Ad, soyad',
        max_length=100,
        null=True, blank=True
    )
    email = models.EmailField(
        'Email ünvanı',
        validators=[validate_email],
        null=True, blank=True
        )
    CV = models.FileField(
        upload_to='vacancy-applications',
        validators=[FileExtensionValidator(['pdf', 'docx'])]
    )
    coverletter = models.TextField(
        'Motivasiya məktubu',
        null=True, blank=True
    )
    prtfolio_website = models.URLField(
        'Portfolio',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Müraciət'
        verbose_name_plural = 'Müraciətlər'

    def __str__(self) -> str:
        return f'NO - {self.pk}{self.vacancy.pk}{self.created_date} müraciət'
    
    @property
    def apply_date(self):
        local_created_date = timezone.localtime(self.created_at)
        return local_created_date.strftime('%d %b %Y, %H:%M')
    
    @property
    def created_date(self):
        local_created_time = timezone.localtime(self.created_at)
        return local_created_time.strftime('%d%m%Y')
    
    def clean(self):
        super().clean()
        current_time = timezone.now()
        if hasattr(self, 'vacancy'):
            if self.vacancy.deadline < current_time:
                raise ValidationError('Müraciətin vaxtı bitib')
        else:
            raise ValidationError('Bu sahə tələb edilir')
        return super().clean()
