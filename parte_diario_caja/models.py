# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from personas import models as m
from .choices import *
from django.core.validators import MaxValueValidator, MinValueValidator


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


class MovimientoCC(models.Model):
    fecha = models.DateField(default=now)
    nro_ingreso = models.BigIntegerField()
    cc = models.ForeignKey('CuentaCorriente', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.nro_ingreso


class DetalleMovimientoCC(models.Model):
    movimiento_cc = models.ForeignKey('MovimientoCC', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.descripcion


class CuentaCorriente(models.Model):
    saldo = models.FloatField()
    titular_cc = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.titular_cc


class ArqueoDiario(models.Model):
    fecha = models.DateTimeField(default=now)
    nro_planilla = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
    billetes_quinientos = models.IntegerField(validators=[MinValueValidator(0)])
    billetes_doscientos = models.IntegerField(validators=[MinValueValidator(0)])
    billetes_cien = models.IntegerField(validators=[MinValueValidator(0)])
    billetes_cincuenta = models.IntegerField(validators=[MinValueValidator(0)])
    billetes_veinte = models.IntegerField(validators=[MinValueValidator(0)])
    billetes_diez = models.IntegerField(validators=[MinValueValidator(0)])
    billetes_cinco = models.IntegerField(validators=[MinValueValidator(0)])
    billetes_dos = models.IntegerField(validators=[MinValueValidator(0)])
    monedas_dos = models.IntegerField(validators=[MinValueValidator(0)])
    monedas_uno = models.IntegerField(validators=[MinValueValidator(0)])
    monedas_cincuenta = models.IntegerField(validators=[MinValueValidator(0)])
    monedas_veinticinco = models.IntegerField(validators=[MinValueValidator(0)])
    debito_credito_cant = models.IntegerField(validators=[MinValueValidator(0)])
    debito_credito_sub = models.FloatField(validators=[MinValueValidator(0)])
    cheques_cant = models.IntegerField(validators=[MinValueValidator(0)])
    cheques_sub = models.FloatField(validators=[MinValueValidator(0)])
    total = models.FloatField()

    def __str__(self):
        return "%s - %s" % (self.fecha, self.nro_planilla)
