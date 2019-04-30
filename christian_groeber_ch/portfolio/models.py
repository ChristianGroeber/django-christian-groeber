from django.db import models
from django.db.models import ForeignKey
from django.shortcuts import get_object_or_404
from froala_editor.fields import FroalaField
from colorfield.fields import ColorField
# Create your models here.


class TimelineElement(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='timeline_element', blank=True)
    text = FroalaField(blank=True)
    date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class Technology(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    logo = models.ImageField(upload_to='technology-logo', blank=True)
    color = ColorField(default='#FF0000')
    background_color = models.CharField(max_length=50, default='rgba(0,0,0,0.5)')

    def __str__(self):
        return self.title

    def get_rgb(self):
        h = str(self.color).lstrip('#')
        h_arr = list(h)
        r = h_arr[0]
        r += h_arr[1]
        g = h_arr[2]
        g += h_arr[3]
        b = h_arr[4]
        b += h_arr[5]
        ret = 'rgba(' + str(int(r, 16)) + ', ' + str(int(g, 16)) + ', ' + str(int(b, 16)) + ', 0.2)'
        self.background_color = ret
        print(self.background_color)
        self.save()
        return ret


class Element(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='portfolio_elements', blank=True)
    text = FroalaField(blank=True)
    files = models.FileField(blank=True)
    subscriptable = models.BooleanField(default=False)
    timeline_elements = models.ManyToManyField(TimelineElement, blank=True)
    technologies = models.ManyToManyField(Technology)
    portfolio_type = models.CharField(max_length=50, blank=True)
    date_started = models.DateField()
    date_finished = models.DateField(null=True, blank=True)

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
