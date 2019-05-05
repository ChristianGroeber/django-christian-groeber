from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog'),
    path('<int:year>/', views.year_post),
    path('<int:year>/<int:month>/', views.month_post),
    path('<int:year>/<int:month>/<int:day>/', views.post, name='post'),
]
