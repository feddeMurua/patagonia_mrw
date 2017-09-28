# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from polymorphic.models import PolymorphicModel


class Localidad(models.Model):
    nombre = models.CharField(max_length=25)
    cp = models.IntegerField()
    provincia = models.ForeignKey('Provincia', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.nombre, self.cp, self.provincia.nombre, self.provincia.nacionalidad)


class Provincia(models.Model):
    nombre = models.CharField(max_length=25)
    nacionalidad = models.ForeignKey('Nacionalidad', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.nombre, self.nacionalidad)


class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return "%s" % self.nombre


class Domicilio(models.Model):
    barrio = models.CharField(max_length=20, null=True, blank=True)
    calle = models.CharField(max_length=50)
    calle_entre1 = models.CharField(max_length=50, null=True, blank=True)
    calle_entre2 = models.CharField(max_length=50, null=True, blank=True)
    nro = models.IntegerField()
    dpto = models.CharField(max_length=2, null=True, blank=True)
    piso = models.IntegerField(null=True, blank=True)
    localidad = models.ForeignKey('Localidad', on_delete=models.CASCADE)

    def __str__(self):
        return "%s, %s %s" % (self.barrio, self.calle, self.nro)


class DomicilioRural(models.Model):
    chacra = models.CharField(max_length=4)
    parcela = models.CharField(max_length=4, null=True, blank=True)
    sector = models.CharField(max_length=3, null=True, blank=True)
    circunscripcion = models.CharField(max_length=3, null=True, blank=True)
    ruta = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return "Chacra %s, sobre ruta %s" % (self.chacra, self.ruta)


class PersonaGenerica(PolymorphicModel):
    nombre = models.CharField(max_length=50)
    domicilio = models.ForeignKey('domicilio')
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return "%s" % self.nombre


class PersonaJuridica(PersonaGenerica):
    cuit = models.CharField(unique=True, max_length=20)

    def __str__(self):
        datos = " - %s" % self.cuit
        return super(PersonaJuridica, self).__str__() + datos


class PersonaFisica(PersonaGenerica):
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(unique=True, max_length=50)
    nacionalidad = models.ForeignKey('Nacionalidad', on_delete=models.CASCADE)
    obra_social = models.CharField(max_length=50, blank=True)
    documentacion_retirada = models.BooleanField(default=False)
    rubro = models.CharField(max_length=50, blank=True)

    def __str__(self):
        datos = " %s - %s" % (self.apellido, self.dni)
        return super(PersonaFisica, self).__str__() + datos


class RolActuante(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return "%s" % self.nombre


class PersonalPropio(PersonaFisica):
    rol_actuante = models.ManyToManyField(RolActuante)

    def __str__(self):
        return super(PersonalPropio, self).__str__()



