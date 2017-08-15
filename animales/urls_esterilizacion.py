from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_esterilizaciones, name='lista_esterilizaciones'),
    url(r'^nuevo$', AltaEsterilizacion.as_view(), name='nueva_esterilizacion')
 ]
