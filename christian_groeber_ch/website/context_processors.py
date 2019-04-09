from .models import Page


def pages(request):
    pages = Page.objects.filter(show_on_page=True)
    return {'pages': pages}
