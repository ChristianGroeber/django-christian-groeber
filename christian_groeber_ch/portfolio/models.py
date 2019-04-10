from django.db import models
from django.shortcuts import get_object_or_404
from froala_editor.fields import FroalaField

# Create your models here.


class TimelineElement(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='timeline_element', blank=True)
    text = FroalaField(blank=True)
    date_of_completion = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class Element(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='portfolio_elements', blank=True)
    text = FroalaField(blank=True)
    files = models.FileField(blank=True)
    subscriptable = models.BooleanField(default=False)
    timeline_elements = models.ManyToManyField(TimelineElement, blank=True)

    def generate_url(self):
        arr = str(self.title).split(' ')
        tmp = ''
        for i in range(len(arr)):
            if i is not 0:
                tmp += '-'
            tmp += arr[i]
        self.url = tmp

    def get_from_url(str):
        arr_type = str.split('-')
        str_type = ''
        for i in range(len(arr_type)):
            if i is not 0:
                str_type += ' '
            str_type += arr_type[i]
        type = get_object_or_404(Element, title=str_type)
        return type

    def __str__(self):
        return self.title


class Type(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    elements = models.ManyToManyField(Element, blank=True)

    def __str__(self):
        return self.title

    def generate_url(self):
        arr = str(self.title).split(' ')
        tmp = ''
        for i in range(len(arr)):
            if i is not 0:
                tmp += '-'
            tmp += arr[i]
        self.type_url = tmp

    def get_from_url(str):
        arr_type = str.split('-')
        str_type = ''
        for i in range(len(arr_type)):
            if i is not 0:
                str_type += ' '
            str_type += arr_type[i]
        type = get_object_or_404(Type, title=str_type)
        return type

