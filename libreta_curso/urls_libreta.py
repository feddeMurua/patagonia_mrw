from django.conf.urls import url

from .views import (
    ListaLibreta,
    DetalleLibreta,
    AltaLibreta,
    BajaLibreta,
    ModificacionLibreta
)

urlpatterns = [

    url(r'^$', ListaLibreta.as_view(), name='lista_libretas'),
    url(r'^(?P<pk>\d+)$', DetalleLibreta.as_view(), name='detalle_libreta'),
    url(r'^nuevo$', AltaLibreta.as_view(), name='nueva_libreta'),
    url(r'^borrar/(?P<pk>\d+)$', BajaLibreta.as_view(), name='borrar_libreta'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionLibreta.as_view(), name='modificar_libreta'),

]
