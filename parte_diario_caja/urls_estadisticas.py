from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^caja$', estadisticas_caja, name='estadisticas_caja'),    
]
