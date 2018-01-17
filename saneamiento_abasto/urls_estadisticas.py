from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^vehiculos$', estadisticas_vehiculos, name='estadisticas_vehiculos'),    
]
