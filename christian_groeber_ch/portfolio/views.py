from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Type, Element, TimelineElement


def portfolio(request):
    types = Type.objects.all()
    for type in types:
        type.generate_url()
    return render(request, 'portfolio/index.html', {'types': types})


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
    return render(request, 'portfolio/portfolio_type.html', {'portfolio_type': type, 'elements': elements})


def element(request, portfolio_type, element):
    p_type = decode_url(Type, portfolio_type)
    elem = decode_url(Element, element)
    content = elem.timeline_elements.all().order_by('-date')
    print(content)
    return render(request, 'portfolio/element.html', {'element': elem, 'type': p_type, 'content': content})
