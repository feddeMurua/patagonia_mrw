# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from personas import models as m
from .choices import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class Abastecedor(m.PersonaFisica):
    empresa = models.CharField(max_length=25, unique=True)
    # POR EL MOMENTO SOLO SE REQUIERE EL NOMBRE

    def __str__(self):
        datos = " - %s" % self.empresa
        return super(Abastecedor, self).__str__() + datos


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
    primer_inspector = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE, related_name="inspector_1")
    # formset inspector o manyto manty
    turno = models.TimeField()
    precintado = models.IntegerField()
    num_certificado = models.BigIntegerField()
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)

    def __str__(self):
        return "%s " % self.fecha


class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    dominio = models.CharField(max_length=50, unique=True)
    titular = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    tsa = models.BooleanField()

    def __str__(self):
        return "%s - %s" % (self.marca, self.dominio)

'''
rubro SI Y NO CON LA EMPRESA (EJ. DON LEON)
CATEGORIA (A,B,C,D)
TRANSPORTE CERRADO, ABIERTO, REFRIGERADO Y CONGELADO
ASOCIAR CATEGOGIRA Y RUBRO
RUBRO QE ESTA EN PERSONA ES PARA LO DEL CARNET!!!!
EN EMPRESA PARA EL ABASTECEDOR ES QE SE RELACIONAN
ABASTACEDORES ES PARA EL EJIDO
TSA DENTRO DE LA CIUDAD O SALE
EN LA REINSPECCION PUEDEN HABER N CANTIDAD DE INSPECTORES (POR AHI 3)
TURNO EN RESPINSPCCION:
MATUTINO, VESPERTINO, SABADO , FERIADO, o,  EXCPECION: FUERA DE HORARIO(COMPUTA DOBLE) (CHOICE) (son 5)
'''


class Desinfeccion(models.Model):
    # todos los meses es obligatoria
    quincena = models.CharField(max_length=30, choices=Quincenas)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)

    def __str__(self):
        return "%s -%s -%s -%s" % (self.fecha, self.quincena, self.vehiculo.dominio, self.vehiculo.titular)
