
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from personas import models as m
from django.utils.timezone import now
from .choices import *


class Abastecedor(models.Model):
    responsable = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.responsable


class ReinspeccionProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    kilo_producto = models.FloatField()
    reinspeccion = models.ForeignKey('Reinspeccion', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.producto.nombre, self.reinspeccion)


class Producto(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return "%s" % self.nombre


class Reinspeccion(models.Model):
    turno = models.DateTimeField()
    inspectores = models.ManyToManyField(m.PersonalPropio)
    precintado = models.IntegerField()
    num_certificado = models.BigIntegerField()
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.abastecedor, self.turno.date())


class Vehiculo(models.Model):
    marca = models.CharField(max_length=15, choices=Marca_vehiculo)
    dominio = models.CharField(max_length=50, unique=True)
    titular = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    tipo_vehiculo = models.CharField(max_length=3, choices=Tipo_Vehiculo, default='TPP')
    disposicion_resolucion = models.CharField(max_length=50, blank=True, null=True, unique=True)
    # SI EL VEHICULO ES TSA
    categoria = models.CharField(max_length=50, choices=Categoria, blank=True, null=True)
    rubro_vehiculo = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.marca, self.dominio)


'''
TURNO EN RESPINSPECCION:
    MATUTINO, VESPERTINO, SABADO, FERIADO, o EXCPECION: FUERA DE HORARIO (COMPUTA DOBLE) (CHOICE) (son 5)
'''


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
    # TENER EN CUENTA CERTIFICADO DE DEUDA
    fecha_hoy = models.DateField(default=now)
    responsable = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE, related_name="responsable_propietario")
    funcionario_actuante = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE, related_name="funcionario")
    tipo_plaga = models.CharField(max_length=50, choices=Plagas)
    procedimiento = models.CharField(max_length=400)  # (aplicacion de producto en el acta)
    recomendaciones = models.CharField(max_length=400, blank=True, null=True)
    fecha_prox_visita = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_hoy, self.responsable, self.tipo_plaga)
