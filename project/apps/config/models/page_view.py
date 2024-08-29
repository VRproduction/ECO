from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PageView(models.Model):
    url = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name = 'page_views')

    class Meta:
        unique_together = ('url', 'ip_address', 'timestamp', 'user')

    def __str__(self):
        return f"{self.url} - {self.ip_address} - {self.timestamp} - {self.user}"

class MonitoredURL(models.Model):
    url_pattern = models.CharField(max_length=255, unique=True, help_text="Regex pattern for URLs to monitor")
    is_monitored = models.BooleanField(default=True, help_text="Whether this URL should be monitored for visits")

    def __str__(self):
        return f"{self.url_pattern} - {'Monitored' if self.is_monitored else 'Not Monitored'}"
