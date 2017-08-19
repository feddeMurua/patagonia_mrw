from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^nueva/(?P<pk>\d+)$', alta_disposicion, name='nueva_disposicion')
]
