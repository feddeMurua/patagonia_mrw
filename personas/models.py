# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class PersonaGenerica(models.Model):
    nombre = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)
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
    nacionalidad = models.CharField(max_length=50)
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

