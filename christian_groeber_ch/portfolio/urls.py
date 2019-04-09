from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    url('<portfolio_type>/', views.spec_portfolio, name='spec_portfolio')
]