# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from personas import models as m
from patentamiento import models as p
from .choices import *


class Analisis(models.Model):
    fecha = models.DateField(default=now)
    nro_ingreso = models.BigIntegerField()
    interesado = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="interesado")
    procedencia = models.CharField(max_length=50)
    medico_veterinario = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE,
                                              related_name="medico_veterinario")
    resultado = models.CharField(max_length=15, choices=Resultados)
    categoria = models.CharField(max_length=15, choices=Categorias)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.nro_ingreso)


class Porcino(models.Model):
    precinto = models.BigIntegerField(unique=True)
    categoria_porcino = models.CharField(max_length=6, choices=Categoria_Porcino)
    analisis = models.ForeignKey('Analisis', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.categoria_porcino, self.precinto)


class ControlAntirrabico(models.Model):
    fecha_suceso = models.DateField(default=now)
    mordido = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE, related_name="mordido")
    responsable = models.OneToOneField(m.PersonaFisica, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name="responsable")
    observaciones = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):
        return "%s " % self.fecha_suceso


class HabilitacionCriaderoCerdos(models.Model):
    interesado = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    # funcionario_actuante ?
    fecha_disposicion = models.DateField()
    nro_disposicion = models.BigIntegerField()

    def __str__(self):
        return "%s - %s" % (self.fecha_disposicion, self.nro_disposicion)


class Esterilizacion(models.Model):
    interesado = models.OneToOneField(m.PersonaGenerica, on_delete=models.CASCADE)
    mascota = models.OneToOneField(p.Mascota, on_delete=models.SET_NULL, null=True, blank=True)
    turno = models.TimeField()

    def __str__(self):
        return "%s - %s" % (self.interesado, self.turno)


class RetiroEntregaAnimal(models.Model):
    observaciones = models.TextField(max_length=200, default='', blank=True)
    interesado = models.OneToOneField(m.PersonaGenerica, on_delete=models.CASCADE)
    mascota = models.OneToOneField(p.Mascota, on_delete=models.SET_NULL, null=True, blank=True)
    # baja logica, se hace sobre la mascota

    def __str__(self):
        return "%s" % self.interesado
