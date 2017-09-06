from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_reinspeccion, name='lista_reinspecciones'),
    url(r'^nueva$', AltaReinspeccion.as_view(), name='nueva_reinspeccion'),
]
