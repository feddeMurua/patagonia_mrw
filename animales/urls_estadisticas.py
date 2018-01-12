from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^animales$', estadisticas_animales, name='estadisticas_animales'),
    url(r'^mascotas$', estadisticas_mascotas, name='estadisticas_mascotas')
]
