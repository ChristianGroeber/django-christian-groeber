from django.shortcuts import render, redirect
from .models import Post


# Create your views here.


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


def year_post(request, year):
    return render(request, 'blog/index.html')


def month_post(request, year, month):
    return render(request, 'blog/index.html')


def post(request, year, month, post_title):
    print(post_title)
    return render(request, 'blog/index.html')
