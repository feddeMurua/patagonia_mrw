# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from personas import models as m
from django.utils.timezone import now
from .choices import *
from django.core.validators import MinValueValidator


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
        return "%s" % self.producto.nombre

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
    turno = models.CharField(max_length=10, choices=Turno_Reinspeccion)
    inspectores = models.ManyToManyField(m.PersonalPropio)
    precintado = models.IntegerField()
    num_certificado = models.BigIntegerField()
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.abastecedor)


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
        return "Cuenta: %s" % self.pk


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
    marca = models.CharField(max_length=15, choices=Marca_vehiculo)
    dominio = models.CharField(max_length=50, unique=True)
    titular = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    tipo_vehiculo = models.CharField(max_length=3, choices=Tipo_Vehiculo, default='TPP')
    tipo_tpp = models.CharField(max_length=15, blank=True, null=True, choices=Tipo_TPP)
    disposicion_resolucion = models.CharField(max_length=50, blank=True, null=True, unique=True)
    categoria = models.CharField(max_length=50, choices=Categoria, blank=True, null=True)
    rubro_vehiculo = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.marca, self.dominio)


class Desinfeccion(models.Model):
    fecha_realizacion = models.DateField(default=now)
    proximo_vencimiento = models.DateField()
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)
    quincena = models.CharField(max_length=30)
    infraccion = models.BooleanField(default=False)
    justificativo = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_realizacion, self.vehiculo, self.vehiculo.titular)


class ControlDePlaga(models.Model):
    fecha_hoy = models.DateField(default=now)
    responsable = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE, related_name="responsable_propietario")
    funcionario_actuante = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE, related_name="funcionario")
    tipo_plaga = models.CharField(max_length=50, choices=Plagas)
    procedimiento = models.CharField(max_length=400)
    recomendaciones = models.CharField(max_length=400, blank=True, null=True)
    fecha_prox_visita = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_hoy, self.responsable, self.tipo_plaga)


class PagoDiferido(models.Model):
    monto = models.FloatField()
    fecha_pago = models.DateField()
    control = models.ForeignKey('ControlDePlaga', on_delete=models.CASCADE)

    def detalles(self, servicio, control):
        self.monto = servicio.importe
        self.control = control
        self.save()
