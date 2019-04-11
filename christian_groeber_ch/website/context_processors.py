from .models import Page
from contact.models import ContactElement


def pages(request):
    pages = Page.objects.filter(show_on_page=True)
    return {'pages': pages}


def social_media(request):
    links = ContactElement.objects.filter(is_social_media=True)
    return {'social_media': links}
