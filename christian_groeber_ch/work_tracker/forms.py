from datetime import timezone, datetime

from django.forms import forms, ModelForm, DateTimeField, DateField, TimeField
from .models import Trackable, CalendarEvent


class CreateProject(ModelForm):
    class Meta:
        model = Trackable
        exclude = ['running', 'current_calendar_event']


class DescriptionForm(ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['description']


class PlanningForm(forms.Form):
    date = DateField(input_formats=["%d.%m.%Y"], initial=datetime.today().strftime("%d.%m.%Y"))
    start_time = TimeField(input_formats=['%H:%M'])
    end_time = TimeField(input_formats=['%H:%M'])
