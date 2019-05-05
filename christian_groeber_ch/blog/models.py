from django.db import models
from django.db.models import Model, CharField
from froala_editor.fields import FroalaField

# Create your models here.
from django.utils import timezone


class Topic(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Post(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500, blank=True)
    date_posted = models.DateTimeField(default=timezone.now())
    main_image = models.ImageField(upload_to='blog', blank=True)
    text = FroalaField()
    author = CharField(max_length=50, default='Christian Gröber')
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.title


def get_posts_by_year(year):
    posts = Post.objects.all()
    year_posts = []
    for post in posts:
        if post.date_posted.year == year:
            year_posts.append(post)
    return year_posts
