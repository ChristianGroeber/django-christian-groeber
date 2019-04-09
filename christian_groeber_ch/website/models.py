from django.db import models

# Create your models here.


class Page(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=50)
    show_on_page = models.BooleanField(default=True)

    def __str__(self):
        return self.title
