from colorfield.fields import ColorField
from django.db import models

# Create your models here.


class Color(models.Model):
    color_id = models.IntegerField()
    foreground_hash_code = models.CharField(max_length=7)
    background_hash_code = models.CharField(max_length=7)

    def __str__(self):
        return str(self.color_id)


class Trackable(models.Model):
    title = models.CharField(max_length=200)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
