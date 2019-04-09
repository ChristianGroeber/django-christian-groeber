from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.


class Element(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='portfolio_elements', blank=True)
    text = FroalaField(blank=True)
    files = models.FileField(blank=True)

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
