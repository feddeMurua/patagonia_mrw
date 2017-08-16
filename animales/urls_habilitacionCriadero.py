from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_habilitaciones, name='lista_habilitaciones'),
    url(r'^nuevo$', AltaHabilitacion.as_view(), name='nueva_habilitacion'),
    url(r'^pdf/(?P<pk>\d+)$', PdfHabilitacion.as_view(), name='pdf_habilitacion'),
 ]
