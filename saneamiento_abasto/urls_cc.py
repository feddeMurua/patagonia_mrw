from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_cc, name='lista_cc'),    
]
