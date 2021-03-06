# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from datetime import datetime
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
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=datetime.now())
    titular = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)
    nro_ingreso = models.BigIntegerField(unique=True)
    forma_pago = models.CharField(max_length=50, choices=TipoPago, default='Efectivo')
    nro_cheque = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "N° Ingresos Varios: %s - %s" % (self.nro_ingreso, self.titular)

    def to_json(self):
        return {'nro_ingreso': self.nro_ingreso, 'titular': self.titular.to_json()}


class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey('MovimientoDiario', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    importe = models.FloatField()
    servicio = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s" % self.descripcion

    def completar(self, servicio, obj):
        self.descripcion = str(servicio) + " | N° " + str(obj.id)
        self.importe = servicio.importe
        self.servicio = str(servicio)
        self.save()

    def completar_monto(self, importe, servicio, obj):
        self.descripcion = servicio + " | N° " + str(obj.id)
        self.importe = importe
        self.servicio = servicio
        self.save()


class ArqueoDiario(models.Model):
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    turno = models.CharField(max_length=10, null=True, choices=Turno, default='Mañana')
    nro_planilla = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
    mil = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    quinientos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    doscientos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cien = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    b_cincuenta = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    veinte = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    diez = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cinco = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    m_dos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    uno = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    m_cincuenta = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    veinticinco = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    tarjeta_cant = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    tarjeta_sub = models.FloatField(default=0, validators=[MinValueValidator(0)])
    cheques_cant = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cheques_sub = models.FloatField(default=0, validators=[MinValueValidator(0)])
    total_manual = models.FloatField(null=True)
    mov_efectivo_sis = models.IntegerField(null=True)
    sub_efectivo_sis = models.FloatField(null=True)
    mov_tarjeta_sis = models.IntegerField(null=True)
    sub_tarjeta_sis = models.FloatField(null=True)
    mov_cheque_sis = models.IntegerField(null=True)
    sub_cheque_sis = models.FloatField(null=True)
    mov_total_sistema = models.IntegerField(null=True)
    imp_total_sistema = models.FloatField(null=True)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.nro_planilla)

    def detalle_sistema(self, datos):
        self.mov_efectivo_sis = datos['efectivo_mov']
        self.sub_efectivo_sis = datos['efectivo_imp']
        self.mov_tarjeta_sis = datos['tarjeta_mov']
        self.sub_tarjeta_sis = datos['tarjeta_imp']
        self.mov_cheque_sis = datos['cheque_mov']
        self.sub_cheque_sis = datos['cheque_imp']
        self.mov_total_sistema = datos['total_mov']
        self.imp_total_sistema = datos['total_imp']
        self.realizado = True
        self.save()

    class Meta:
        unique_together = ("fecha", "turno")
