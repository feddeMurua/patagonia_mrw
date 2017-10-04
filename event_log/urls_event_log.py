from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_eventos, name='lista_eventos'),
]
