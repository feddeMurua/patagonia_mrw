from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_esterilizaciones, name='lista_esterilizaciones'),
    url(r'^nuevo$', alta_esterilizacion, name='nueva_esterilizacion'),
    url(r'^nuevo/noPatentado$', alta_esterilizacion_nopatentado, name='nueva_esterilizacion_nopatentado'),
    url(r'^consentimiento/(?P<pk_esterilizacion>\d+)$', PdfConsentimiento.as_view(), name='pdf_consentimiento'),

    # url(r'^getMascotas/(?P<pk_interesado>\d+)$', get_mascotas, name="get_mascotas"),
 ]
