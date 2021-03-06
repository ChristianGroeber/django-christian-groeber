from django.shortcuts import render, redirect
from .models import Post, Topic
from . import models


# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-date_posted')
    posts_2019 = models.get_posts_by_year(2019)
    return render(request, 'blog/index.html', {'posts': posts, 'posts_2019': posts_2019})


def year_post(request, year):
    posts = models.get_posts_by_year(year)
    return render(request, 'blog/index.html', {'posts_2019': posts, 'year': year})


def post(request, year, month, post_title):
    post = Post.objects.get(title=post_title)
    return render(request, 'blog/blog.html', {'post': post})


def topic(request, topic):
    topic_obj = Topic.objects.get(title=topic)
    posts = models.get_post_from_topic(topic_obj)
    return render(request, 'blog/topic.html', {'topic': topic_obj, 'posts': posts})
