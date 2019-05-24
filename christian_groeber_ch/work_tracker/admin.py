from django.contrib import admin
from .models import Trackable, Color, CalendarEvent

# Register your models here.


admin.site.register(Trackable)
admin.site.register(Color)
admin.site.register(CalendarEvent)
