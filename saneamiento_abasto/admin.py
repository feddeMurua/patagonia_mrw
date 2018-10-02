# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import *
from solo.admin import SingletonModelAdmin

admin.site.register(Abastecedor)
admin.site.register(Reinspeccion)
admin.site.register(ReinspeccionProducto)
admin.site.register(CuentaCorriente)
admin.site.register(DetalleCC)
admin.site.register(Producto)
admin.site.register(Vehiculo)
admin.site.register(MarcaVehiculo)
admin.site.register(Desinfeccion)
admin.site.register(ControlDePlaga)
admin.site.register(VisitaControl)
admin.site.register(PagoDiferido)
admin.site.register(ReinspeccionPrecios, SingletonModelAdmin)
