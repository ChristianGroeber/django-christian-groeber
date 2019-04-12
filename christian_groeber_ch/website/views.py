from django.http import HttpResponse
from django.shortcuts import render
from christian_groeber_ch.settings import STATICFILES_DIRS

# Create your views here.


def index(request):
    return render(request, 'website/index.html')


def csr(request):
    print(STATICFILES_DIRS)
    f = open(STATICFILES_DIRS[0] + '/csr/C3D56FF12F47C32F673F55F046ADFE3C.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")
