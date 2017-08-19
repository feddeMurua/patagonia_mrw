# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


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
    nombre = models.CharField(max_length=25)
    
    def __str__(self):
        return "%s" % self.nombre


class Domicilio(models.Model):
    barrio = models.CharField(max_length=20)
    calle = models.CharField(max_length=50)
    nro = models.IntegerField()
    dpto = models.CharField(max_length=2, null=True, blank=True)
    piso = models.IntegerField(null=True, blank=True) 
    localidad = models.ForeignKey('Localidad', on_delete=models.CASCADE)

    def __str__(self):
        return "%s, %s %s" % (self.barrio, self.calle, self.nro)
        # TENER EN CUENTA CASO DEPARTAMENTOS.


class PersonaGenerica(models.Model):
    nombre = models.CharField(max_length=50)
    domicilio = models.ForeignKey('Domicilio')
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True)
    rubro = models.CharField(max_length=50)
    
    def __str__(self):
        return "%s" % self.nombre


class PersonaJuridica(PersonaGenerica):
    cuil = models.CharField(unique=True, max_length=20)

    def __str__(self):
        datos = " %s" % self.cuil
        return super(PersonaJuridica, self).__str__() + datos


class PersonaFisica(PersonaGenerica):    
    apellido = models.CharField(max_length=50)    
    fecha_nacimiento = models.DateField()
    dni = models.CharField(unique=True, max_length=50)
    nacionalidad = models.OneToOneField('Nacionalidad', on_delete=models.CASCADE)
    obra_social = models.CharField(max_length=50, blank=True)
    documentacion_retirada = models.BooleanField(default=False)

    def __str__(self):
        datos = " %s - %s" % (self.apellido, self.dni)
        return super(PersonaFisica, self).__str__() + datos
        

class PersonalPropio(PersonaFisica):
    rol_actuante = models.CharField(max_length=50)  
        
    def __str__(self):
            datos = " - %s" % self.rol_actuante
            return super(PersonalPropio, self).__str__() + datos    
