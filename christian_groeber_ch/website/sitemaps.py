from django.contrib.sitemaps import Sitemap
from portfolio.models import Type, Element, Technology


class TypeSitemap(Sitemap):

    def items(self):
        return Type.objects.all()


class ElementSitemap(Sitemap):

    def items(self):
        return Element.objects.all()


class TechnologySitemap(Sitemap):

    def items(self):
        return Technology.objects.all()
