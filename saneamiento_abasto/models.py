# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from personas import models as m


class Abastecedor(models.Model):
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    empresa_y_o_transporte = models.CharField(max_length=150)
    rubro = models.CharField(max_length=150)

    def __str__(self):
        return "%s - %s" % (self.persona, self.rubro)


class ReinspeccionProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    kilo_producto =  models.FloatField()
    reinspeccion = models.ForeignKey('Reinspeccion', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.nombre, self.reinspeccion)


class Producto(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return "%s " % self.nombre


class Reinspeccion(models.Model):
    #FALTA MONTO POR INSPECCION, CUANDO SE DISEÑOE EL ARQUEO DE CAJA, AGREGAR.
    fecha = models.DateField()
    primer_inspector = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="inspector_1")
    segundo_inspector = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="inspector_2", null=True, blank=True)
    turno = models.TimeField()
    precintado = models.IntegerField()
    num_certificado = models.BigIntegerField()
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)

    def __str__(self):
        return "%s " % (self.fecha)

class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    dominio = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s" % (self.marca, self.dominio)


class Tsa_Tpp (models.Model): #PREGUNTA: UN TSA PUEDE ESTAR EN MULTIPLES ABASTACEDORES?
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE, null=True, blank=True)
    #SI EL ABASTECEDOR ES NULL, SE PUEDE CONSIDERAR TPP (transporte puúblico de perosnas)
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="persona", null=True, blank=True)
    #LA PERSONA PUEDE SER NULL, PORQUE SI ES ABASTECEDOR, YA ESTA REGISTRADA EN EL SISTEMA
    vehiculo = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="vehiculo")

    def __str__(self):
        return "%s" % (self.vehiculo)
