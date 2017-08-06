# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from desarrollo_patagonia import models as m
from django.utils.timezone import now
from libreta_curso import models as m

class Analisis(models.Model):
	fecha = models.DateField(default=now)
	nro_ingreso =  models.BigIntegerField()
	interesado = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, primary_key=True)
	procedencia = models.CharField(max_length=50)
	medico_veterinario = models.CharField(max_length=50)	
	resultado = models.BooleanField()

	def __str__(self):
		return "%s - %s" % (self.fecha, self.nro_ingreso)

class Animal(models.Model):
	categoria = models.CharField(max_length=50)
	precinto = models.BigIntegerField(unique=True)
	analisis = models.ForeignKey('Analisis', on_delete=models.CASCADE)

	def __str__(self):
		return "%s - %s" % (self.categoria, self.precinto)