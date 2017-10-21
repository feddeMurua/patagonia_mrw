# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .choices import *
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from personas import models as m
import os


def get_image_path(instance, filename):
    return os.path.join('images/', str(instance.pk), filename)


class LibretaSanitaria(models.Model):
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True, blank=True)
    observaciones = models.TextField(max_length=200, default='', blank=True)
    fecha_examen_clinico = models.DateField()
    profesional_examen_clinico = models.CharField(max_length=200, default='')
    lugar_examen_clinico = models.CharField(max_length=200, default='')
    fecha = models.DateField(default=now)
    foto = models.ImageField(upload_to='', blank=True)

    def __str__(self):
        return "Libreta Sanitaria N°: %s - %s" % (self.pk, self.persona)


class Curso(models.Model):
    fecha_inicio = models.DateTimeField()
    cupo = models.IntegerField(validators=[MaxValueValidator(500), MinValueValidator(1)])
    lugar = models.CharField(max_length=50)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return "Curso Nro: %s - %s" % (self.pk, self.fecha_inicio.date())


class Inscripcion(models.Model):
    fecha_inscripcion = models.DateField(default=now)
    modificado = models.BooleanField(default=False)
    nota_curso = models.CharField(max_length=15, choices=Calificaciones, blank=True)
    porcentaje_asistencia = models.FloatField(null=True, blank=True)
    observaciones = models.TextField(max_length=200, default='', blank=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    persona = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)

    def __str__(self):
        return "Inscripcion Nro: %s" % self.pk
