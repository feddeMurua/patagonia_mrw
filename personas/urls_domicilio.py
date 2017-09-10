from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^nueva$', alta_localidad, name='nueva_localidad'),
    url(r'^getProvincias$', get_provincias, name='get_provincias'),
]
