# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.db import models
from django.utils.timezone import now
from desarrollo_patagonia import models as m
import os


def get_image_path(instance, filename):
    return os.path.join('images/', str(instance.pk), filename)


class PersonaFisica(m.PersonaGenerica):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cuil = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(unique=True,max_length=50)
    nacionalidad = models.CharField(max_length=50)
    obra_social = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "%s, %s - %s" % (self.apellido, self.nombre, self.dni)


class LibretaSanitaria(models.Model):
    nro_ingresos_varios = models.BigIntegerField(null=True, blank=True)
    arancel = models.FloatField(null=True, blank=True)
    persona = models.OneToOneField('PersonaFisica', on_delete=models.CASCADE, primary_key=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True,blank=True)
    observaciones = models.CharField(max_length=200, default='',blank=True)
    examen_clinico = models.ForeignKey('ExamenClinico', on_delete=models.CASCADE)
    fecha = models.DateField(default=now)
    foto = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.pk, self.persona)


class ExamenClinico(models.Model):
    fecha = models.DateField()
    profesional = models.CharField(max_length=50)
    centro_atencion = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s %s" % (self.fecha, self.profesional, self.centro_atencion)


class Curso(models.Model):
    fecha_inicio = models.DateField()
    cupo = models.IntegerField()
    lugar = models.CharField(max_length=50)
    horario= models.TimeField()
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.fecha_inicio


class Inscripcion(models.Model):
    nota_curso = models.IntegerField(null=True, blank=True)
    porcentaje_asistencia = models.FloatField(null=True, blank=True)
    nro_ingresos_varios = models.BigIntegerField(null=True, blank=True)
    arancel = models.FloatField(null=True, blank=True)
    observaciones = models.CharField(max_length=200, default='', blank=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    persona = models.OneToOneField('PersonaFisica', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "Numero inscripcion:%s" % self.pk
