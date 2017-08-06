from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^detalle/(?P<pk>\d+)/(?P<id_curso>\d+)$', DetalleInscripcion.as_view(), name='detalle_inscripcion'),
    url(r'^pdf/(?P<pk>\d+)/(?P<id_curso>\d+)$', PdfInscripcion.as_view(), name='pdf_inscripcion'),
    url(r'^nueva/(?P<id_curso>\d+)$', AltaInscripcion.as_view(), name='nueva_inscripcion'),
    url(r'^borrar/(?P<pk>\d+)/(?P<id_curso>\d+)$', BajaInscripcion.as_view(), name='borrar_inscripcion'),
    url(r'^editar/(?P<pk>\d+)/(?P<id_curso>\d+)$', ModificacionInscripcion.as_view(), name='modificar_inscripcion'),
]
