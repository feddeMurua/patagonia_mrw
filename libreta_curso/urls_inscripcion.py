from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^pdf/(?P<pk>\d+)$', PdfInscripcion.as_view(), name='pdf_inscripcion'),
    url(r'^nueva/(?P<id_curso>\d+)$', alta_inscripcion, name='nueva_inscripcion'),
    url(r'^borrar/(?P<pk>\d+)/(?P<id_curso>\d+)$', BajaInscripcion.as_view(), name='borrar_inscripcion'),
    url(r'^editar/(?P<pk>\d+)/(?P<id_curso>\d+)$', ModificacionInscripcion.as_view(), name='modificar_inscripcion'),
]
