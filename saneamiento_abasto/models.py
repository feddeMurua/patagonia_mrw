# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from personas import models as m
from .choices import *


class Abastecedor(models.Model):
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    empresa = models.ForeignKey(m.PersonaJuridica, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s -%s" % (self.persona, self.empresa)


class ReinspeccionProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    kilo_producto = models.FloatField()
    reinspeccion = models.ForeignKey('Reinspeccion', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.producto.nombre, self.reinspeccion)


class Producto(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return "%s " % self.nombre


class Reinspeccion(models.Model):
    # FALTA MONTO POR INSPECCION, CUANDO SE DISEÑE EL ARQUEO DE CAJA, AGREGAR.
    fecha = models.DateField()
    primer_inspector = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="inspector_1")
    segundo_inspector = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="inspector_2",
                                             null=True, blank=True)
    turno = models.TimeField()
    precintado = models.IntegerField()
    num_certificado = models.BigIntegerField()
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)

    def __str__(self):
        return "%s " % self.fecha


class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    dominio = models.CharField(max_length=50)
    # UN AUTO NO PUEDE SER TSA Y TPP

    def __str__(self):
        return "%s - %s" % (self.marca, self.dominio)


class Transporte(models.Model):
    vehiculo = models.OneToOneField('Vehiculo', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.vehiculo


class Tsa (Transporte):
    # TRANSPORTE DE SUSTANCIA ALIMENTICIAS
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, null=True, blank=True)
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE, null=True, blank=True)
    # PREGUNTA: UN TSA PUEDE ESTAR EN MULTIPLES ABASTACEDORES? NO! solo importa un solo lado.
    # (abastecedores-> muchos tsa)

    def __str__(self):
        return "%s " % self.persona


class Tpp(Transporte):
    # TRANSPORTE PUBLICO DE PERSONAS
    persona = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.persona


class Desinfeccion(models.Model):
    # todos los meses es obligatoria
    quincena = models.CharField(max_length=30, choices=Quincenas)
    transporte = models.ForeignKey('Transporte', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return "%s -%s -%s" % (self.quincena, self.transporte, self.fecha)
