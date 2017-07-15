from django.conf.urls import url
from django_filters.views import FilterView
from .filters import CursoListFilter
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
    url(r'^buscar/$', FilterView.as_view(filterset_class=CursoListFilter,
        template_name='curso/curso_search.html'), name='buscar_curso'),
]
