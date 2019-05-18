from PIL import Image, ExifTags
from django.db import models
from django.db.models import ForeignKey
from django.shortcuts import get_object_or_404
from froala_editor.fields import FroalaField
from colorfield.fields import ColorField
from martor.models import MartorField
# Create your models here.


class TimelineElement(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='timeline_element', blank=True)
    text = MartorField(blank=True)
    date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Technology(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    logo = models.ImageField(upload_to='technology-logo', blank=True)
    color = ColorField(default='#FF0000')
    background_color = models.CharField(max_length=50, default='rgba(0,0,0,0.5)')
    skill_level = IntegerRangeField(min_value=1, max_value=10)
    html_class = models.CharField(max_length=100, blank=True)
    importance = models.IntegerField()

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

    def set_html_class(self):
        self.html_class = self.title
        if ' ' in self.html_class:
            ret = ''
            for i in range(len(str(self.html_class).split(' '))):
                if i is not 0:
                    ret += '-'
                ret += str(self.html_class).split(' ')[i]
            self.html_class = ret
            self.save()


class GalleryElement(models.Model):
    title = models.CharField(max_length=50, default='Image')
    file = models.ImageField(upload_to='gallery')
    thumbnail = models.ImageField(upload_to='gallery/thumbs', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args):
        super(GalleryElement, self).save(force_update=False)
        img = Image.open(self.file.path)
        thumb = Image.open(self.thumbnail.path)
        exif = dict((ExifTags.TAGS[k], v) for k, v in img._getexif().items() if k in ExifTags.TAGS)
        if not exif['Orientation'] or exif['Orientation'] is 8:
            img = img.rotate(90, expand=True)
            thumb = thumb.rotate(90, expand=True)
        else:
            print(exif['Orientation'])
        thumb.thumbnail((300, 300), Image.ANTIALIAS)
        img.save(self.file.path)
        print(self.thumbnail.path)
        thumb.save(self.thumbnail.path)


class Element(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='portfolio_elements', blank=True)
    text = MartorField(blank=True)
    files = models.FileField(blank=True)
    subscriptable = models.BooleanField(default=False)
    timeline_elements = models.ManyToManyField(TimelineElement, blank=True)
    technologies = models.ManyToManyField(Technology)
    portfolio_type = models.CharField(max_length=50, blank=True)
    date_started = models.DateField()
    date_finished = models.DateField(null=True, blank=True)
    gallery_elements = models.ManyToManyField(GalleryElement, blank=True)
    github = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, blank=True)
    include_in_resume = models.BooleanField(default=True)

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
    is_gallery = models.BooleanField(default=False)

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
