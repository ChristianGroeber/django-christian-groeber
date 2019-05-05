from django.shortcuts import render, redirect
from .models import Post
from . import models


# Create your views here.


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


def year_post(request, year):
    posts = models.get_posts_by_year(year)
    return render(request, 'blog/index.html', {'year_posts': posts})


def month_post(request, year, month):
    return render(request, 'blog/index.html')


def post(request, year, month, post_title):
    print(post_title)
    post = Post.objects.get(title=post_title)
    return render(request, 'blog/post.html', {'post': post_title})
