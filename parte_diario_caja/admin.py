# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

admin.site.register(TipoServicio)
admin.site.register(Servicio)
admin.site.register(DetalleMovimiento)
admin.site.register(MovimientoDiario)
