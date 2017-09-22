# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from personas import models as m
from django.utils.timezone import now
from .choices import *


class Abastecedor(m.PersonaFisica):
    empresa = models.CharField(max_length=25, blank=True, null=True)
    categoria = models.CharField(max_length=500, choices=Categoria)
    rubro_abastecedor = models.CharField(max_length=150)

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
        return "%s" % self.nombre


class Reinspeccion(models.Model):
    # FALTA MONTO POR INSPECCION, CUANDO SE DISEÑE EL ARQUEO DE CAJA, AGREGAR.
    turno = models.DateTimeField()
    inspectores = models.ManyToManyField(m.PersonalPropio)
    precintado = models.IntegerField()
    num_certificado = models.BigIntegerField()
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.turno


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
ASOCIAR CATEGORIA Y RUBRO:

1 transporte isotérmico con equipo de frio para transportar productos congelados.
(productos carneos, aves. pescados, mariscos, hielo, helados)

2 transporte isotérmico con equipo de frio para transportar productos refrigerados.
(productos carneos, aves, fiambres, lacteos, pastas, productos del mar, sandwiches, productos de rotisería)

3 transporte isotérmico de productos envasados que no requieran refrigeración.
(bebidas, aguas, panificación y afines)

4 transporte con caja abierta y protección mediante lona o toldo.
(frutas, verduras, huevos, bebidas)

5 otros.

***tener en cuenta qe se puede tener otros agregados


EN EMPRESA PARA EL ABASTECEDOR ES QUE SE RELACIONAN
 - ABASTACEDORES ES PARA EL EJIDO
 - TSA DENTRO DE LA CIUDAD O SALE
TURNO EN RESPINSPECCION:
    MATUTINO, VESPERTINO, SABADO, FERIADO, o EXCPECION: FUERA DE HORARIO (COMPUTA DOBLE) (CHOICE) (son 5)
'''


class Desinfeccion(models.Model):
    quincena = models.CharField(max_length=30, choices=Quincenas)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s" % (self.quincena, self.vehiculo.dominio, self.vehiculo.titular)


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
        return "%s - %s - %s" % (self.fecha_hoy, self.responsable.dominio, self.tipo_plaga)
