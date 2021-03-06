from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('technology/<technology>/', views.technology),
    path('Photography/<gallery_element>/<img_id>/', views.image),
    path('Photography/<gallery_element>/<img_id>/prev/', views.prev_image),
    path('Photography/<gallery_element>/<img_id>/next/', views.next_image),
    path('<portfolio_type>/', views.spec_portfolio, name='spec_portfolio'),
    path('<portfolio_type>/<element>/', views.element, name='element'),
]
