from django.forms import forms, ModelForm
from .models import Trackable, CalendarEvent


class CreateProject(ModelForm):
    class Meta:
        model = Trackable
        exclude = ['running', 'current_calendar_event']


class DescriptionForm(ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['description']
