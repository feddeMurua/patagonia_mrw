from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_curso, name='lista_cursos'),
    url(r'^nuevo$', alta_curso, name='nuevo_curso'),
    url(r'^borrar/(?P<pk>\d+)$', baja_curso, name='borrar_curso'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_curso, name='modificar_curso'),
    url(r'^inscripciones/(?P<id_curso>\d+)$', lista_inscripciones_curso, name='inscripciones_curso'),
    url(r'^cierre/(?P<id_curso>\d+)$', cierre_de_curso, name='cierre_curso'),
    url(r'^pdf_asistencia/(?P<pk>\d+)$', PdfAsistencia.as_view(), name='pdf_asistencia'),
    url(r'^pdf_aprobados/(?P<pk>\d+)$', PdfAprobados.as_view(), name='pdf_aprobados')
]
