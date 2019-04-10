from django.db import models
from django.db.models import CharField, Model

# Create your models here.


class ContactElement(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500, blank=True)
    link = models.URLField()
    icon = models.ImageField(upload_to='contact_icon', blank=True)
    is_social_media = models.BooleanField(default=False)

    def __str__(self):
        return self.title
