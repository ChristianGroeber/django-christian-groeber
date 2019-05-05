from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog'),
    path('<int:year>/', views.year_post),
    path('<int:year>/<int:month>/<post_title>/', views.post, name='post'),
]
