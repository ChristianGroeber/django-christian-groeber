from django.shortcuts import render

# Create your views here.
from .models import ContactElement


def index(request):
    types = ContactElement.objects.all()
    return render(request, 'contact/index.html', {'types': types})
