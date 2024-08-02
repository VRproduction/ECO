import datetime
from django.contrib.sites.models import Site

from apps.config.models.general_settings import *

def is_active_time():
    general_setting = GeneralSettings.objects.first()
    current_time = datetime.datetime.now()

    if general_setting:
        if current_time.minute == 0:
            return general_setting.work_start_hour.hour <= current_time.hour <= general_setting.work_finish_hour.hour
        else:
            return general_setting.work_start_hour.hour < current_time.hour < general_setting.work_finish_hour.hour
