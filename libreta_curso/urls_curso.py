from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_curso, name='lista_cursos'),
    url(r'^nuevo$', AltaCurso.as_view(), name='nuevo_curso'),
    url(r'^borrar/(?P<pk>\d+)$', baja_curso, name='borrar_curso'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionCurso.as_view(), name='modificar_curso'),
    url(r'^inscripciones/(?P<id_curso>\d+)$', lista_inscripciones_curso, name='inscripciones_curso'),
    url(r'^cierre/(?P<id_curso>\d+)$', cierre_de_curso, name='cierre_curso'),
    url(r'^cierre/(?P<id_curso>\d+)/inscripcion/(?P<pk>\d+)$', CierreCursoInscripcion.as_view(), name='cierre_inscripcion_curso'),

]
