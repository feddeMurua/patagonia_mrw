from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_detalle_movimientos, name='lista_detalle_movimientos'),    
]
