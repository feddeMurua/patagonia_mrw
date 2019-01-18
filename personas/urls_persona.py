from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^contribuyentes', lista_contribuyentes, name='lista_contribuyentes'),

    url(r'^fisicas/nueva$', alta_p_fisica, name='nueva_persona_fisica'),
    url(r'^fisicas/(?P<pk>\d+)$', detalle_persona_fisica, name='detalle_persona_fisica'),
    url(r'^fisicas/borrar/(?P<pk>\d+)$', baja_persona_fisica, name='borrar_persona_fisica'),
    url(r'^fisicas/editar/(?P<pk>\d+)$', modificacion_persona_fisica, name='modificar_persona_fisica'),

    url(r'^juridicas/nueva$', alta_p_juridica, name='nueva_persona_juridica'),
    url(r'^juridicas/(?P<pk>\d+)$', DetallePersonaJuridica.as_view(), name='detalle_persona_juridica'),
    url(r'^juridicas/borrar/(?P<pk>\d+)$', baja_persona_juridica, name='borrar_persona_juridica'),
    url(r'^juridicas/editar/(?P<pk>\d+)$', modificacion_persona_juridica, name='modificar_persona_juridica'),

    url(r'^personal_propio$', lista_personal_propio, name='lista_personal_propio'),
    url(r'^personal_propio/nuevo$', alta_p_propio, name='nuevo_personal_propio'),
    url(r'^personal_propio/(?P<pk>\d+)$', DetallePersonalPropio.as_view(), name='detalle_personal_propio'),
    url(r'^personal_propio/borrar/(?P<pk>\d+)$', baja_personal_propio, name='borrar_personal_propio'),
    url(r'^personal_propio/editar/(?P<pk>\d+)$', modificacion_personal_propio, name='modificar_personal_propio'),

    url(r'^domicilio/nueva_localidad/$', AltaLocalidad.as_view(), name='nueva_localidad'),
    url(r'^domicilio/nueva_provincia/$', AltaProvincia.as_view(), name='nueva_provincia'),
    url(r'^domicilio/nueva_nacionalidad/$', AltaNacionalidad.as_view(), name='nueva_nacionalidad'),

    url(r'^verificar/documento/$', verificar_documento, name='verificar_documento'),

]
