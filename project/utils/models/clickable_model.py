from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from apps.tracking.models import IPAddress, ClickTracking

class ClickableModel(models.Model):
    click_count = models.PositiveIntegerField(default=0)
    click_tracking = GenericRelation(ClickTracking)

    class Meta:
        abstract = True

    def record_click(self, ip_address):
        content_type = ContentType.objects.get_for_model(self)
        click_tracking, created = ClickTracking.objects.get_or_create(
            content_type=content_type,
            object_id=self.id,
        )

        if not IPAddress.objects.filter(click_tracking=click_tracking, ip_address=ip_address).exists():
            IPAddress.objects.create(click_tracking=click_tracking, ip_address=ip_address)
            click_tracking.click_count += 1
            click_tracking.save()  # Save the updated click_count to ClickTracking
            self.click_count += 1
            self.save()  # Save the updated click_count to Clickable model

    # def get_click_count(self):
    #     content_type = ContentType.objects.get_for_model(self)
    #     click_tracking = ClickTracking.objects.filter(
    #         content_type=content_type,
    #         object_id=self.id
    #     ).first()
    #     return click_tracking.click_count if click_tracking else 0