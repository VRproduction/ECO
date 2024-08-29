import re
from apps.config.models import PageView, MonitoredURL
from django.utils import timezone

class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'GET':
            full_path = request.build_absolute_uri()
            ip_address = self.get_client_ip(request)
            user = request.user if request.user.is_authenticated else None

            monitored_urls = MonitoredURL.objects.filter(is_monitored=True).values_list('url_pattern', flat=True)

            if full_path in monitored_urls:
                PageView.objects.update_or_create(
                    url=full_path,
                    ip_address=ip_address,
                    user=user,
                    defaults={'timestamp': timezone.now()}
                )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
