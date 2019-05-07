from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('muttertag/', views.muttertag, name='muttertag'),
]
