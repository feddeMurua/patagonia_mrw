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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.inicio, name="inicio"),
    url(r'^cursos/', include('libreta_curso.urls_curso', namespace='cursos')),
    url(r'^libretas/', include('libreta_curso.urls_libreta', namespace='libretas')),
    url(r'^personas/', include('libreta_curso.urls_persona', namespace='personas')),
    url(r'^examenes/', include('libreta_curso.urls_examen', namespace='examenes')),
    url(r'^inscripciones/', include('libreta_curso.urls_inscripcion', namespace='inscripciones')),
]
