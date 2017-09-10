from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_tsa, name='lista_tsa'),
    url(r'^nuevo_tsa$', AltaTsa.as_view(), name='nuevo_tsa'),
    url(r'^$', lista_tpp, name='lista_tpp'),
    url(r'^nuevo_tpp$', AltaTpp.as_view(), name='nuevo_tpp'),
]
