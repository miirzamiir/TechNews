from django.db import models
from .utils.persian_calendar import PersianCalendar


class Tag(models.Model):
    tag_label = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.tag_label


class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    tags = models.ManyToManyField(to=Tag)
    resource = models.URLField(blank=False, unique=True)
    date = models.DateTimeField(default=PersianCalendar.currnet_persian_datetime, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = PersianCalendar.currnet_persian_datetime()
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title