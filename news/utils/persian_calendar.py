import datetime
import jdatetime
from django.utils import timezone

class PersianCalendar:

    @classmethod
    def currnet_persian_datetime(cls):
        current_timezone = timezone.get_current_timezone()
        current = jdatetime.datetime.now()
        return timezone.make_aware(datetime.datetime(current.year, current.month, current.day, current.hour, current.minute), current_timezone)
