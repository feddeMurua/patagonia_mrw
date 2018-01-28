# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from solo.models import SingletonModel
from parte_diario_caja import models as pd_m
from personas import models as m
from .choices import *


class Abastecedor(models.Model):
    responsable = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Abastecedor, self).save(*args, **kwargs)
        CuentaCorriente.objects.create(abastecedor=self)

    def __str__(self):
        return "%s" % self.responsable


class ReinspeccionProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    kilo_producto = models.FloatField()
    reinspeccion = models.ForeignKey('Reinspeccion', on_delete=models.CASCADE)

    def __str__(self):
        return "%s || %s" % (self.producto.nombre, self.reinspeccion)

    def to_json(self):
        return {
            'producto': {'nombre': self.producto.nombre},
            'kilo_producto': self.kilo_producto
        }


class Producto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return "%s" % self.nombre

    def to_json(self):
        return {'nombre': self.nombre}


class Reinspeccion(models.Model):
    fecha = models.DateField(default=now)
    turno = models.CharField(max_length=10, choices=TURNO_REINSPECCION)
    inspectores = models.ManyToManyField(m.PersonalPropio)
    precintado = models.IntegerField()
    num_certificado = models.BigIntegerField()
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.abastecedor)


class ReinspeccionPrecios(SingletonModel):
    kg_min = models.IntegerField(validators=[MinValueValidator(1)], default=30)
    precio_min = models.FloatField(validators=[MinValueValidator(0)], default=55)
    precio_kg = models.FloatField(validators=[MinValueValidator(0)], default=0.25)

    def __unicode__(self):
        return u"Precios Vigentes Reinspeccion"

    class Meta:
        verbose_name = "Precios Vigentes Reinspeccion"


'''
CUENTAS CORRIENTES
'''


class DetalleCC(models.Model):
    detalle = models.ForeignKey('Reinspeccion', on_delete=models.CASCADE)
    monto = models.FloatField()
    cc = models.ForeignKey('CuentaCorriente', on_delete=models.CASCADE)

    def __str__(self):
        return "%s, Saldo: %s" % (self.detalle, self.monto)


class CuentaCorriente(models.Model):
    saldo = models.FloatField(default=0)
    abastecedor = models.OneToOneField('Abastecedor', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Cuenta: %s - %s" % (self.pk, self.abastecedor)


class PagoCC(models.Model):
    fecha = models.DateField(default=now)
    monto = models.FloatField(validators=[MinValueValidator(0)])
    cc = models.ForeignKey('CuentaCorriente', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.fecha


'''
VEHICULO Y DESINFECCIONES
'''


class Vehiculo(models.Model):
    marca = models.CharField(max_length=15, choices=MARCA_VEHICULO)
    dominio = models.CharField(max_length=50, unique=True)
    titular = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    tipo_vehiculo = models.CharField(max_length=3, choices=TIPO_VEHICULO, default='TPP')
    tipo_tpp = models.CharField(max_length=15, blank=True, null=True, choices=TIPO_TPP)
    disposicion_resolucion = models.CharField(max_length=50, blank=True, null=True, unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA, blank=True, null=True)
    rubro_vehiculo = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.marca, self.dominio)


class Desinfeccion(models.Model):
    fecha_realizacion = models.DateField(default=now)
    proximo_vencimiento = models.DateField()
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)
    quincena = models.CharField(max_length=30)
    justificativo = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_realizacion, self.vehiculo, self.vehiculo.titular)


class ControlDePlaga(models.Model):
    fecha_hoy = models.DateField(default=now)
    responsable = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE, related_name="responsable_propietario")
    funcionario_actuante = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE, related_name="funcionario")
    tipo_plaga = models.CharField(max_length=50, choices=PLAGAS)
    procedimiento = models.CharField(max_length=400)
    recomendaciones = models.CharField(max_length=400, blank=True, null=True)
    fecha_prox_visita = models.DateField(blank=True, null=True)
    pagado = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_hoy, self.responsable, self.tipo_plaga)


class PagoDiferido(models.Model):
    monto = models.FloatField()
    fecha_pago = models.CharField(max_length=15, choices=PAGO_DIFERIDO)
    control = models.ForeignKey('ControlDePlaga', on_delete=models.CASCADE)

    def detalles(self, nombre_servicio, control):
        servicio = pd_m.Servicio.objects.get(nombre=nombre_servicio)
        self.monto = servicio.importe
        self.control = control
        self.save()

    def __str__(self):
        return "%s - %s - %s" % (self.control.responsable, self.control.tipo_plaga, self.fecha_pago)
