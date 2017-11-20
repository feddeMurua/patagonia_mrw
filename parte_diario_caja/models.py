# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from personas import models as m
from .choices import *


class TipoServicio(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    importe = models.FloatField()
    tipo = models.ForeignKey('TipoServicio', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.nombre


# 18-10-17: Titular se paso de DetalleMovimiento a Movimiento


class MovimientoDiario(models.Model):
    fecha = models.DateField(default=now)
    titular = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)
    nro_ingreso = models.BigIntegerField()

    def __str__(self):
        return "N° Ingresos Varios: %s" % self.nro_ingreso


class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey('MovimientoDiario', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    forma_pago = models.CharField(max_length=50, choices=TipoPago, default='Efectivo')
    nro_cheque = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s" % self.descripcion

    def agregar_detalle(self, movimiento, servicio, descrip):
        self.servicio = servicio
        self.movimiento = movimiento
        self.descripcion = descrip
