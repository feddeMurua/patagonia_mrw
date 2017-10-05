# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import *
from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login$', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    url(r'^logout$', LogoutView.as_view(next_page=reverse_lazy('inicio')), name='logout'),
    url(r'^usuario/cambio_password$',
        CustomPasswordChangeView.as_view(template_name='usuarios/cambio_contraseña.html'), name='cambio_password'),
    url(r'^usuario/cambio_password_hecho$',
        PasswordChangeDoneView.as_view(template_name='usuarios/confirm_cambio_contraseña.html'),
        name='cambio_password_hecho'),
    url(r'^$', inicio, name="inicio"),
    url(r'^cursos/', include('libreta_curso.urls_curso', namespace='cursos')),
    url(r'^libretas/', include('libreta_curso.urls_libreta', namespace='libretas')),
    url(r'^inscripciones/', include('libreta_curso.urls_inscripcion', namespace='inscripciones')),
    url(r'^personas/', include('personas.urls_persona', namespace='personas')),
    url(r'^analisis/', include('animales.urls_analisis', namespace='analisis')),
    url(r'^criadero/', include('animales.urls_criadero', namespace='criadero')),
    url(r'^esterilizaciones/', include('animales.urls_esterilizacion', namespace='esterilizacion')),
    url(r'^patentes/', include('animales.urls_patentes', namespace='patentes')),
    url(r'^controles/', include('animales.urls_controlAntirrabico', namespace='controles')),
    url(r'^retiros_entregas/', include('animales.urls_retiroEntrega', namespace='retiros_entregas')),
    url(r'^abastecedores/', include('saneamiento_abasto.urls_abastecedor', namespace='abastecedores')),
    url(r'^reinspecciones/', include('saneamiento_abasto.urls_reinspeccion', namespace='reinspecciones')),
    url(r'^vehiculos/', include('saneamiento_abasto.urls_vehiculo', namespace='vehiculo')),
    url(r'^desinfecciones/', include('saneamiento_abasto.urls_desinfecciones', namespace='desinfecciones')),
    url(r'^controles/plagas/', include('saneamiento_abasto.urls_controlPlaga', namespace='controles_plagas')),
    url(r'^caja/', include('parte_diario_caja.urls_caja', namespace='caja')),
    url(r'^eventos/', include('event_log.urls_event_log', namespace='event_log')),
]
