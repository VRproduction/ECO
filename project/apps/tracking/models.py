from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ClickTracking(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    click_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add = True, null = True)
    updated = models.DateTimeField(auto_now = True, null = True)

    class Meta:
        unique_together = ('content_type', 'object_id')

class IPAddress(models.Model):
    click_tracking = models.ForeignKey(ClickTracking, on_delete=models.CASCADE, related_name='ip_addresses')
    ip_address = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add = True, null = True)
    updated = models.DateTimeField(auto_now = True, null = True)

    class Meta:
        unique_together = ('click_tracking', 'ip_address')
