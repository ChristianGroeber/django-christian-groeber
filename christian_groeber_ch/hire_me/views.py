from django.shortcuts import render, redirect
from portfolio.models import Element
from .models import Resume, Experience


# Create your views here.


def index(request):
    resume = Resume.objects.get(pk=1)
    experiences = resume.experiences.all().order_by('-date_from')
    return render(request, 'hire_me/index.html', {'resume': resume, 'experiences': experiences})
