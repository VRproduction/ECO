from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import validate_email
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField
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
        default=timezone.now()
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
        return local_created_time.strftime('%d/%m/%Y, %H:%M')
    
    @property
    def published_date(self):
        local_published_time = timezone.localtime(self.published_at)
        return local_published_time.strftime('%d.%m.%Y')
    

class IPs(models.Model):
    view_ip = models.GenericIPAddressField('IP ünvanı', editable=False)

    class Meta:
        verbose_name = ('IP ünvanı')
        verbose_name_plural = ('IP ünvanları')

    def __str__(self) -> str:
        return self.view_ip
    

class CompanyDepartment(models.Model):
    department_name = models.CharField('Şöbənin adı', max_length=200)

    class Meta:
        verbose_name = 'Şöbə'
        verbose_name_plural = 'Şöbələr'

    def __str__(self) -> str:
        return self.department_name
    

class JobType(models.Model):
    job_type = models.CharField('Məşğulluğun növü', max_length=200)

    class Meta:
        verbose_name = 'Məşğulluq növü'
        verbose_name_plural = 'Məşğulluq növləri'

    def __str__(self) -> str:
        return self.job_type


class WorkingHour(models.Model):
    start_date = models.TimeField(
        'İşin başlama saatı', 
        default=timezone.now()
    )
    end_date = models.TimeField(
        'İşin bitmə saatı', 
        default=timezone.now()
    )

    class Meta:
        verbose_name = 'İş qrafiki'
        verbose_name_plural = 'İş qrafikləri'

    def __str__(self) -> str:
        return f'{self.start} - {self.end}'
    
    @property
    def start(self):
        return self.start_date.strftime('%H:%M')
    
    @property
    def end(self):
        return self.end_date.strftime('%H:%M')
    

class VacancyType(models.Model):
    vacancy_type = models.CharField('Elanın növü', max_length=200)

    class Meta:
        verbose_name = 'Elanın növü'
        verbose_name_plural = 'Elanın növləri'

    def __str__(self) -> str:
        return self.vacancy_type
    

class Vacancy(Base):
    vacancy_title = models.CharField('Vakant yerin adı', max_length=200)
    vacancy_content = RichTextUploadingField(
        'Vakansiyanın təsviri',
        null=True,
        blank=True
    )
    salary = models.IntegerField(
        'Əmək haqqı', 
        default=345
    )
    deadline = models.DateTimeField(
        'Son müraciət tarixi', 
        default=timezone.now()
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
    job_type = models.ForeignKey(
        JobType,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Məşğulluq növü',
        null=True,
        blank=True
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
    def deadline_date(self):
        local_deadline = timezone.localtime(self.deadline)
        return local_deadline.strftime('%d %b %Y')
    
    def get_absolute_url(self):
        return reverse('vacancy-detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.vacancy_title)
        super().save(*args, **kwargs)
    

# class VacancyApplication(Base):
#     created_at = models.DateTimeField(
#         'Müraciətin edilmə tarixi', 
#         auto_now_add=True
#     )
#     vacancy = models.ForeignKey(
#         Vacancy,
#         on_delete=models.CASCADE,
#         related_name='applications',
#         verbose_name='Elan'
#     )
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(validators=[validate_email])
#     CV = models.FileField(
#         upload_to='vacancy-applications'
#     )

#     class Meta:
#         verbose_name = 'Müraciət'
#         verbose_name_plural = 'Mwraciətlər'

#     def __str__(self) -> str:
#         return f'Müraciət => {self.vacancy} '

