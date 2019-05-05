from django.db import models
from django.db.models import Model, CharField
from froala_editor.fields import FroalaField

# Create your models here.
from django.utils import timezone


class Post(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500, blank=True)
    date_posted = models.DateTimeField(default=timezone.now())
    main_image = models.ImageField(upload_to='blog', blank=True)
    text = FroalaField()
    author = CharField(max_length=50, default='Christian Gröber')

    def __str__(self):
        return self.title
