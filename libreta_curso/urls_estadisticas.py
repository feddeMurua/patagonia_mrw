from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^libretas_cursos$', estadisticas_lc, name='estadisticas_lc')
]
