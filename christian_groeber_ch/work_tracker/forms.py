from django.forms import forms, ModelForm
from .models import Trackable


class CreateProject(ModelForm):
    class Meta:
        model = Trackable
        exclude = ['running', 'current_calendar_event']
