from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^transporte_desinfecciones/$', estadisticas_TD, name='estadisticas_TD'),
    url(r'^reinspeccion/$', estadisticas_reinspeccion, name='estadisticas_reinspeccion'),        
]
