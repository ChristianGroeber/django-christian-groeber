from django.shortcuts import render, redirect
from .models import Post
from . import models


# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-date_posted')
    posts_2019 = models.get_posts_by_year(2019)
    return render(request, 'blog/index.html', {'posts': posts, 'posts_2019': posts_2019})


def year_post(request, year):
    posts = models.get_posts_by_year(year)
    return render(request, 'blog/index.html', {'year_posts': posts, 'year': year})


def month_post(request, year, month):
    posts = models.get_posts_by_month(year, month)
    return render(request, 'blog/index.html', {'month_posts': posts, 'month': posts[0].date_posted})


def post(request, year, month, post_title):
    post = Post.objects.get(title=post_title)
    return render(request, 'blog/blog.html', {'post': post})
