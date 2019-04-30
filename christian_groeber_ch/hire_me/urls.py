from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='hire-me'),
]
