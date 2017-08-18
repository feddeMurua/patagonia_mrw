# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(PersonaFisica)
admin.site.register(Domicilio)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(Nacionalidad)
admin.site.register(PersonaJuridica)
admin.site.register(PersonalPropio)

