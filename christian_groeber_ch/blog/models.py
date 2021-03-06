from django.db import models
from django.db.models import Model, CharField

# Create your models here.
from django.utils import timezone
from martor.models import MartorField


class Topic(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Post(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    main_image = models.ImageField(upload_to='blog', blank=True)
    text = MartorField()
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


def get_post_from_topic(topic):
    posts = []
    for post in Post.objects.all().order_by('-date_posted'):
        if topic in post.topics.all():
            posts.append(post)
    return posts
