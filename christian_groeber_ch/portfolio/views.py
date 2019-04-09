from django.shortcuts import render

# Create your views here.
from .models import Type


def portfolio(request):
    types = Type.objects.all()
    print(types)
    return render(request, 'portfolio/index.html', {'types': types})
