# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from personas import models as m
from .choices import *


class Analisis(models.Model):
    fecha = models.DateField(default=now)
    nro_ingreso =  models.BigIntegerField()
    interesado = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="interesado")
    procedencia = models.CharField(max_length=50)
    medico_veterinario = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="medico_veterinario")
    resultado = models.CharField(max_length=15, choices=Resultados)
    categoria = models.CharField(max_length=15, choices=Categorias)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.nro_ingreso)


class Animal(models.Model):	
    precinto = models.BigIntegerField(unique=True)
    analisis = models.ForeignKey('Analisis', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.analisis.categoria, self.precinto)