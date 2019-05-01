from django.contrib import admin

# Register your models here.
from .models import Element, Type, TimelineElement, Technology, GalleryElement

admin.site.register(Type)
admin.site.register(Element)
admin.site.register(TimelineElement)
admin.site.register(Technology)
admin.site.register(GalleryElement)
