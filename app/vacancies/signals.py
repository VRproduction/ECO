from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.translation import gettext as _

from product.utils.custom_slugify import custom_az_slugify
from vacancies.models import (
    VacancyApplication,
    Vacancy, VacancyType,
    WorkingHour, JobType,
    CompanyDepartment

)


@receiver(post_save, sender=VacancyApplication)
def notify_super_user(sender, created, instance, **kwargs):
    if created:
        site = Site.objects.get_current()
        domain = site.domain
        title = _("Ecoproduct.az, yeni vakansiya müraciəti var!")
        data = {
            'vacancy_application': instance,
            'domain': domain,
        }
        message = render_to_string('mail/new_vacancy_application_email.html', data)
        send_mail(
            title, 
            message,
            settings.EMAIL_HOST_USER,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False, html_message=message
        )   

@receiver(pre_save, sender=Vacancy)
def make_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = custom_az_slugify(instance.vacancy_title)

@receiver(pre_save, sender=VacancyType)
def make_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = custom_az_slugify(instance.vacancy_type)

@receiver(pre_save, sender=Vacancy)
def make_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = custom_az_slugify(instance.vacancy_type)

@receiver(pre_save, sender=WorkingHour)
def make_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = custom_az_slugify(instance.work_hour)

@receiver(pre_save, sender=JobType)
def make_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = custom_az_slugify(instance.job_type)

@receiver(pre_save, sender=CompanyDepartment)
def make_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = custom_az_slugify(instance.department_name)