from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from vacancies.models import (
    VacancyApplication
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