# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class PersonaGenerica(models.Model):
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)
    rubro = models.CharField(max_length=50)

    class Meta:
        abstract = True


class PersonaFisica(PersonaGenerica):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cuil = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(unique=True, max_length=50)
    nacionalidad = models.CharField(max_length=50)
    obra_social = models.CharField(max_length=50, blank=True)
    documentacion_retirada = models.BooleanField(default=False)

    def __str__(self):
        return "%s, %s - %s" % (self.apellido, self.nombre, self.dni)
