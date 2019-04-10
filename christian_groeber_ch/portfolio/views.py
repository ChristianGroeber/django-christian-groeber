from django.shortcuts import render, redirect

# Create your views here.
from .models import Type


def portfolio(request):
    types = Type.objects.all()
    for type in types:
        type.generate_url()
    return render(request, 'portfolio/index.html', {'types': types})


def spec_portfolio(request, portfolio_type):
    return render(request, 'portfolio/portfolio_type.html', {'portfolio_type':portfolio_type})
