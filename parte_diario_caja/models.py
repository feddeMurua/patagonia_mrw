# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from personas import models as m
from .choices import *
from django.core.validators import MinValueValidator


class TipoServicio(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    importe = models.FloatField(validators=[MinValueValidator(0)])
    tipo = models.ForeignKey('TipoServicio', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.nombre


class MovimientoDiario(models.Model):
    fecha = models.DateField(default=now)
    titular = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)
    nro_ingreso = models.BigIntegerField(unique=True)
    forma_pago = models.CharField(max_length=50, choices=TipoPago, default='Efectivo')
    nro_cheque = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "N° Ingresos Varios: %s - %s" % (self.nro_ingreso, self.titular)


class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey('MovimientoDiario', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.descripcion


class ArqueoDiario(models.Model):
    fecha = models.DateTimeField(default=now)
    nro_planilla = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
    billetes_quinientos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    billetes_doscientos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    billetes_cien = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    billetes_cincuenta = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    billetes_veinte = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    billetes_diez = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    billetes_cinco = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    billetes_dos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    monedas_dos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    monedas_uno = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    monedas_cincuenta = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    monedas_veinticinco = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    debito_credito_cant = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    debito_credito_sub = models.FloatField(default=0, validators=[MinValueValidator(0)])
    cheques_cant = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cheques_sub = models.FloatField(default=0, validators=[MinValueValidator(0)])
    mov_efectivo_sis = models.IntegerField()
    sub_efectivo_sis = models.FloatField()
    mov_tarjeta_sis = models.IntegerField()
    sub_tarjeta_sis = models.FloatField()
    mov_cheque_sis = models.IntegerField()
    sub_cheque_sis = models.FloatField()
    total_manual = models.FloatField()
    total_sistema = models.FloatField()

    def __str__(self):
        return "%s - %s" % (self.fecha, self.nro_planilla)

    def detalle_sistema(self, datos):
        self.mov_efectivo_sis = datos.cant_efectivo
        self.sub_efectivo_sis = datos.sub_efectivo
        self.mov_tarjeta_sis = datos.cant_tarjeta
        self.sub_tarjeta_sis = datos.sub_tarjeta
        self.mov_cheque_sis = datos.cant_cheque
        self.sub_cheque_sis = datos.sub_cheque
        self.total_sistema = datos.total
