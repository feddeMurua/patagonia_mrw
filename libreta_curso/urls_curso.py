from django.conf.urls import url

from .views import (
    ListaCurso,
    DetalleCurso,
    AltaCurso,
    BajaCurso,
    ModificacionCurso
)

urlpatterns = [

    url(r'^$', ListaCurso.as_view(), name='lista_cursos'),
    url(r'^(?P<pk>\d+)$', DetalleCurso.as_view(), name='detalle_curso'),
    url(r'^nuevo$', AltaCurso.as_view(), name='nuevo_curso'),
    url(r'^borrar/(?P<pk>\d+)$', BajaCurso.as_view(), name='borrar_curso'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionCurso.as_view(), name='modificar_curso'),
]
