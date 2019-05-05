from django.shortcuts import render, redirect


# Create your views here.


def index(request):
    return render(request, 'blog/index.html')


def year_post(request, year):
    return render(request, 'blog/index.html')


def month_post(request, year, month):
    return render(request, 'blog/index.html')


def post(request, year, month, day):
    print(year)
    return render(request, 'blog/index.html')
