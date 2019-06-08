from colorfield.fields import ColorField
from django.db import models

# Create your models here.


class Color(models.Model):
    color_id = models.IntegerField()
    foreground_hash_code = models.CharField(max_length=7)
    background_hash_code = models.CharField(max_length=7)

    def __str__(self):
        return str(self.color_id)


class CalendarEvent(models.Model):
    summary = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True)
    event_id = models.CharField(max_length=200)

    def __str__(self):
        return self.event_id


class Trackable(models.Model):
    title = models.CharField(max_length=200)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    running = models.BooleanField(default=False)
    current_calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title


class MyUser(models.Model):
    name = models.CharField(max_length=200)
    trackables = models.ManyToManyField(Trackable)

    def __str__(self):
        return self.name
