from django.shortcuts import render

# Create your views here.
from .models import Type


def portfolio(request):
    types = Type.objects.all()
    for type in types:
        type.generate_url()
    return render(request, 'portfolio/index.html', {'types': types})
