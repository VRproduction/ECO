from django.db import models
import datetime

class WeekDay(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)
    is_workday = models.BooleanField(default=True)
    work_start_hour = models.TimeField(default=datetime.time(9, 0))  # Default to 9 AM
    work_finish_hour = models.TimeField(default=datetime.time(17, 0))  # Default to 5 PM

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {'Workday' if self.is_workday else 'Non-workday'}"
