"""desarrollo_patagonia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from . import views
from saneamiento_abasto import views as sa

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.inicio, name="inicio"),
    url(r'^cursos/', include('libreta_curso.urls_curso', namespace='cursos')),
    url(r'^libretas/', include('libreta_curso.urls_libreta', namespace='libretas')),
    url(r'^inscripciones/', include('libreta_curso.urls_inscripcion', namespace='inscripciones')),
    url(r'^personas/', include('personas.urls_persona', namespace='personas')),
    url(r'^domicilios/', include('personas.urls_domicilio', namespace='domicilios')),
    url(r'^analisis/', include('animales.urls_analisis', namespace='analisis')),
    url(r'^solicitudes/', include('animales.urls_solicitudCriadero', namespace='solicitud')),
    url(r'^disposiciones/', include('animales.urls_disposicionCriadero', namespace='disposicion')),
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

    url(r'^getRubros/(?P<id_categoria>\w+)$', sa.get_rubros, name='get_rubros'),
]
