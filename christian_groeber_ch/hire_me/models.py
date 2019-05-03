from django.db import models
from django.db.models import Model, CharField, ImageField
from froala_editor.fields import FroalaField

from portfolio.models import Element

# Create your models here.


class Experience(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500, blank=True)
    date_from = models.DateField()
    date_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.date_from) + " - " + str(self.title)


class Resume(Model):
    title = CharField(max_length=50, default='resume')
    whoami = FroalaField()
    services = FroalaField()
    experiences = models.ManyToManyField(Experience, blank=True)

    def __str__(self):
        return 'Resume'
