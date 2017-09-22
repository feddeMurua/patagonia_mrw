# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from personas import models as m
from .choices import *
# Create your models here.

class DetalleMovimiento(models.Model):
    codigo = models.BigIntegerField()
    detalle = models.CharField(max_length=100)


class MoviemientoDiario(models.Model):
    fecha = models.DateField(default=now)
    nro_ingreso = models.BigIntegerField(primary=True)
    importe = models.FloatField()
    detalle = models.ForeignKey('DetalleMovimiento', on_delete=models.CASCADE)
    titular = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=50, choices=TipoPago)
    nro_cheque = models.CharField(max_length=100, blank=True, null=True)
