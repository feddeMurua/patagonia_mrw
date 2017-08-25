from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_controles, name='lista_controles'),
    url(r'^nuevo$', alta_control, name='nuevo_control'),
]
