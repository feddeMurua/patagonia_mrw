# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .choices import *
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from personas import models as m


class LibretaSanitaria(models.Model):
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True, blank=True)
    observaciones = models.TextField(max_length=200, default='', blank=True)
    fecha_examen_clinico = models.DateField(null=True)
    profesional_examen_clinico = models.CharField(max_length=200)
    lugar_examen_clinico = models.CharField(max_length=200)
    fecha = models.DateField(default=now)
    tipo_libreta = models.CharField(max_length=10, choices=Tipo_Libreta)
    fecha_vencimiento = models.DateField(null=True)
    foto = models.ImageField(upload_to='libreta_curso/foto/', blank=True)
    pendiente = models.BooleanField(default=False)

    def __str__(self):
        return "Libreta Sanitaria N°: %s - %s" % (self.pk, self.persona)


class Curso(models.Model):
    fecha = models.DateField()
    cupo = models.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(1)])
    lugar = models.CharField(max_length=50)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return "Curso Nro: %s - %s" % (self.pk, self.fecha)


class Inscripcion(models.Model):
    fecha_inscripcion = models.DateField(default=now)
    modificado = models.BooleanField(default=False)
    calificacion = models.CharField(max_length=15, choices=Calificaciones, blank=True)
    porcentaje_asistencia = models.FloatField(null=True, blank=True)
    observaciones = models.TextField(max_length=200, default='', blank=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    persona = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    rubro = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Inscripcion Nro: %s" % self.pk

    def to_json(self):
        return {'fecha_inscripcion': self.fecha_inscripcion.isoformat(), 'observaciones': self.observaciones,
                'calificacion': self.calificacion, 'porcentaje_asistencia': self.porcentaje_asistencia,
                'persona': {'apellido': self.persona.apellido, 'nombre': self.persona.nombre, 'dni': self.persona.dni},
                'rubro': self.rubro}
