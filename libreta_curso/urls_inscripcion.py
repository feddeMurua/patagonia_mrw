from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^pdf/(?P<pk>\d+)$', pdf_inscripcion, name='pdf_inscripcion'),
    url(r'^nueva/(?P<id_curso>\d+)$', alta_inscripcion, name='nueva_inscripcion'),
    url(r'^borrar/(?P<pk>\d+)$', baja_inscripcion, name='borrar_inscripcion'),
    url(r'^modificar/(?P<pk>\d+)/(?P<id_curso>\d+)$', modificacion_inscripcion, name='modificar_inscripcion'),
    url(r'^editar/cierre/(?P<pk>\d+)/(?P<id_curso>\d+)$', cierre_inscripcion, name='cierre_inscripcion'),
]
