from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Type


def portfolio(request):
    types = Type.objects.all()
    for type in types:
        type.generate_url()
    return render(request, 'portfolio/index.html', {'types': types})


def spec_portfolio(request, portfolio_type):
    if '-' not in portfolio_type:
        type = get_object_or_404(Type, title=portfolio_type)
    else:
        type = Type.get_from_url(portfolio_type)
    return render(request, 'portfolio/portfolio_type.html', {'portfolio_type': type})
