from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Type, Element, TimelineElement, Technology


def portfolio(request):
    types = Type.objects.all()
    technologies = Technology.objects.all()
    for technology in technologies:
        technology.get_rgb()
    for type in types:
        type.generate_url()
    return render(request, 'portfolio/index.html', {'types': types, 'technologies': technologies})


def decode_url(cls: object, str: object) -> object:
    if '-' not in str:
        ret = get_object_or_404(cls, title=str)
    else:
        ret = cls.get_from_url(str)
    return ret


def spec_portfolio(request, portfolio_type):
    type = decode_url(Type, portfolio_type)
    elements = type.elements.all()
    for element in elements:
        element.generate_url()
        for technology in element.technologies.all():
            technology.get_rgb()
    return render(request, 'portfolio/portfolio_type.html', {'portfolio_type': type, 'elements': elements})


def element(request, portfolio_type, element):
    p_type = decode_url(Type, portfolio_type)
    type_obj = Type.objects.get(title=p_type)
    elem = decode_url(Element, element)
    # content = elem.timeline_elements.all().order_by('-date')
    content = None
    return render(request, 'portfolio/element.html', {'element': elem, 'type': p_type, 'content': content, 'is_gallery': type_obj.is_gallery})


def technology(request, technology):
    technology = Technology.objects.get(title=technology)
    all_elements = Element.objects.all()
    elements = []
    types = Type.objects.all()
    for element in all_elements:
        if technology in element.technologies.all():
            elements.append(element)
            element.generate_url()
            get_portfolio_type_from_element(element, request)
    return render(request, 'portfolio/technology.html', {'technology': technology, 'elements': elements})


def get_portfolio_type_from_element(element, request):
    for type in Type.objects.all():
        if element in type.elements.all():
            element.portfolio_type = type.title
            element.save()
            break
