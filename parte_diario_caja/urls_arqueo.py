from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_arqueos, name='lista_arqueos'),
    url(r'^nuevo$', alta_arqueo, name='nuevo_arqueo'),
]
