from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'.well-known/pki-validation/C3D56FF12F47C32F673F55F046ADFE3C.txt', views.csr),
]
