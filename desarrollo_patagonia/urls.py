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
from libreta_curso import views as lc_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cursos/', lc_views.ListaCurso.as_view(), name='lista_cursos'),
    url(r'^(?P<pk>\d+)$', lc_views.DetalleCurso.as_view(), name='detalle_curso'),
    url(r'^nuevo$',lc_views.AltaCurso.as_view(), name='nuevo_curso'),
    url(r'^borrar/(?P<pk>\d+)$', lc_views.BajaCurso.as_view(), name='borrar_curso'),
    url(r'^editar/(?P<pk>\d+)$', lc_views.ModificacionCurso.as_view(), name='modificar_curso'),

]
