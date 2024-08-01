from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab, timedelta  # timedelta'yi de ekleyin

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
app = Celery("settings")

# We are using Asia/Baku time so we are making it False
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Baku')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

app.conf.beat_schedule = {
    # 'daily_prepare_and_send_post_message': {
    #     'task': 'core.tasks.daily_prepare_and_send_post_message',
    #     'schedule': timedelta(seconds=15),  # Her dakika çalışacak şekilde ayarlandı
    # }
}

