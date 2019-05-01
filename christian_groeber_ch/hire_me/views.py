import time

from django.shortcuts import render, redirect
from portfolio.models import Element, Technology
from .models import Resume, Experience
import datetime
import portfolio.views


# Create your views here.


def index(request):
    resume = Resume.objects.get(pk=1)
    exp = resume.experiences.all().order_by('-date_from')
    elements = Element.objects.all().order_by('-date_started')
    experiences = []
    for experience in exp:
        experiences.append(ExperienceObject(experience.title, experience.date_from, 'experience', description=experience.description,
                                            date_until=experience.date_until))
    for element in elements:
        element.generate_url()
        experiences.append(ExperienceObject(element.title, element.date_started, 'element', description=element.description,
                                            date_until=element.date_finished, url=element.portfolio_type + '/' + element.url, portfolio_type=element.portfolio_type, technologies=element.technologies.all()))
        portfolio.views.get_portfolio_type_from_element(element, request)
    sorted_experiences = sorted(experiences, key=lambda test: test.date_from)
    date_now = datetime.date.today()
    birthday = datetime.date(1998, 9, 17)
    diff_years = date_now.year - birthday.year
    if date_now.month - birthday.month < 0:
        diff_years -= 1
    elif date_now.day - birthday.day < 0:
        diff_years -= 1
    skills = Technology.objects.all()
    return render(request, 'hire_me/index.html', {'resume': resume, 'experiences': sorted_experiences, 'skills': skills})


class ExperienceObject:
    def __init__(self, title, date_from, exp_type, description=None, date_until=None, url=None, portfolio_type=None, technologies=None):
        self.title = title
        self.date_from = date_from
        self.description = description
        self.date_until = date_until
        self.exp_type = exp_type
        self.url = url
        self.portfolio_type = portfolio_type
        self.technologies = technologies
