from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_desinfecciones, name='lista_desinfecciones'),
    url(r'^nueva_desinfeccion$', AltaDesinfeccion.as_view(), name='nueva_desinfeccion'),
]
