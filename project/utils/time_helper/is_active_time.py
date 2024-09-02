import datetime
from django.utils import timezone
from apps.config.models import WeekDay  

def is_active_time():
    current_time = datetime.datetime.now()
    current_weekday = current_time.weekday()
    try:
        weekday = WeekDay.objects.get(day_of_week=current_weekday)
    except WeekDay.DoesNotExist:
        return False
    if weekday.is_workday:
        if current_time.minute == 0:
            return weekday.work_start_hour.hour <= current_time.hour <= weekday.work_finish_hour.hour
        else:
            return weekday.work_start_hour.hour < current_time.hour <= weekday.work_finish_hour.hour
   
    return False

