# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from personas import models as m
from .choices import *
# Create your models here.

class Servicio(models.Model):
    codigo = models.IntegerField(primary_key=True)
    descrip = models.CharField(max_length=100)
    importe = models.FloatField()
    '''
    ID      DESCRIP     IMPORTE
    1       PATENTE     $130
    '''
    def __str__(self):
        return "%s" % self.descrip


class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey('MoviemientoDiario', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    titular = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=50)
    nro_cheque = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s" % self.descripcion

    def agregar_detalle(self, movimiento, servicio, descrip, titular):
        self.servicio = servicio
        self.movimiento = movimiento
        self.descripcion = descrip
        self.titular = titular


class MoviemientoDiario(models.Model):
    fecha = models.DateField(default=now)
    nro_ingreso = models.BigIntegerField()

    def __str__(self):
        return "%s" % self.fecha
