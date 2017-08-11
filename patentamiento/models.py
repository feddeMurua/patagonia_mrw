# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .choices import *
from django.utils.timezone import now
from personas import models as m


class Mascota(models.Model):
	nombre = models.CharField(max_length=50)
	pelaje = models.CharField(max_length=50)
	raza = models.CharField(max_length=50)
	sexo = models.CharField(max_length=15, choices=Sexo, blank=True)
	fecha_nacimiento = models.DateField(blank=True, null=True)
	baja = models.BooleanField(default=False)
	def __str__(self):
		return "%s %s" % (self.nombre, self.raza)


class Patente(models.Model):
	nro_ingresos_varios = models.BigIntegerField()
	fecha = models.DateField(default=now)
	arancel = models.FloatField()
	persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
	mascota= models.OneToOneField('Mascota', on_delete=models.CASCADE)
	observaciones = models.TextField(max_length=200, default='', blank=True)
	
	def __str__(self):
		return "%s %s" % (self.fecha, self.persona)


class Beneficio(models.Model):
	patente = models.ForeignKey('Patente', on_delete=models.CASCADE)
	fecha_antiparasitario = models.DateField()
	fecha_garrapaticida = models.DateField()
	observaciones = models.TextField(max_length=200, default='', blank=True)