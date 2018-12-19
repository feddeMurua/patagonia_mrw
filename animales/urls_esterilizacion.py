from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_esterilizaciones, name='lista_esterilizaciones'),
    url(r'^nuevo$', alta_esterilizacion, name='nueva_esterilizacion'),
    url(r'^borrar/(?P<pk>\d+)$', baja_esterilizacion, name='borrar_esterilizacion'),
    url(r'^nuevo/noPatentado$', alta_esterilizacion_nopatentado, name='nueva_esterilizacion_nopatentado'),
    url(r'^consentimiento/(?P<pk>\d+)$', pdf_consentimiento, name='pdf_consentimiento'),
    url(r'^confirmar/(?P<pk>\d+)$', confirmar_esterilizacion, name='confirmar_esterilizacion'),
 ]
