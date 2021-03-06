# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from polymorphic.models import PolymorphicModel
from django.core.validators import MinValueValidator
from .choices import *


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
    calle = models.CharField(max_length=50, null=True, blank=True)
    calle_entre1 = models.CharField(max_length=50, null=True, blank=True)
    calle_entre2 = models.CharField(max_length=50, null=True, blank=True)
    nro = models.IntegerField(null=True, blank=True)
    dpto = models.CharField(max_length=50, null=True, blank=True)
    piso = models.IntegerField(null=True, blank=True)
    edificio = models.CharField(max_length=50, null=True, blank=True)
    escalera = models.CharField(max_length=50, null=True, blank=True)
    localidad = models.ForeignKey('Localidad', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.calle, self.nro)


class DomicilioRural(models.Model):
    chacra = models.CharField(max_length=6)
    parcela = models.CharField(max_length=4, null=True, blank=True)
    sector = models.CharField(max_length=3, null=True, blank=True)
    circunscripcion = models.CharField(max_length=3, null=True, blank=True)
    ruta = models.CharField(max_length=25, null=True, blank=True)
    km = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)

    def __str__(self):
        return "Chacra N°: %s" % self.chacra


class PersonaGenerica(PolymorphicModel):
    nombre = models.CharField(max_length=50)
    domicilio = models.ForeignKey('Domicilio')
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return "%s" % self.nombre

    def to_json(self):
        return {'nombre': self.nombre}


class PersonaJuridica(PersonaGenerica):
    cuit = models.CharField(unique=True, max_length=20)

    def __str__(self):
        datos = " - %s" % self.cuit
        return super(PersonaJuridica, self).__str__() + datos

    def to_json(self):
        return {'nombre': self.nombre}


class PersonaFisica(PersonaGenerica):
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    tipo_dni = models.CharField(max_length=10, choices=Tipo_Dni, default='DNI')
    dni = models.CharField(max_length=50)
    nacionalidad = models.ForeignKey('Nacionalidad', on_delete=models.CASCADE)
    obra_social = models.CharField(max_length=50, blank=True)
    documentacion_retirada = models.BooleanField(default=False)

    def __str__(self):
        apellido = "%s, " % self.apellido
        tipo_dni = " - %s" % self.tipo_dni
        dni = " - %s" % self.dni
        return apellido + super(PersonaFisica, self).__str__() + tipo_dni + dni

    class Meta:
        unique_together = ("tipo_dni", "dni")

    def to_json(self):
        return {'nombre': self.apellido + ", " + self.nombre}


class RolActuante(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return "%s" % self.nombre


class PersonalPropio(PersonaFisica):
    rol_actuante = models.ManyToManyField(RolActuante)

    def __str__(self):
        return super(PersonalPropio, self).__str__()
