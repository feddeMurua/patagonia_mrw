# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from personas import models as m
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


class DisposicionCriaderoCerdos(models.Model):
    fecha_disposicion = models.DateField()
    nro_disposicion = models.BigIntegerField()
    solicitud = models.OneToOneField('SolicitudCriaderoCerdos', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.fecha_disposicion, self.nro_disposicion)


class SolicitudCriaderoCerdos(models.Model):
    fecha_solicitud = models.DateField(default=now)
    interesado = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    categoria_criadero = models.CharField(max_length=50, choices=Categoria_Criadero)
    domicilio_criadero = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, default='En curso')

    def __str__(self):
        return "%s - %s" % (self.fecha_solicitud, self.interesado)


class AplazoSolicitud(models.Model):
    fecha_aplazo = models.DateField(default=now)
    motivo_aplazo = models.TextField(max_length=200)
    solicitud = models.OneToOneField('SolicitudCriaderoCerdos', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.fecha_aplazo, self.motivo_aplazo)


class Esterilizacion(models.Model):
    interesado = models.OneToOneField(m.PersonaGenerica, on_delete=models.CASCADE)
    mascota = models.OneToOneField('Mascota', on_delete=models.SET_NULL, null=True, blank=True)
    turno = models.TimeField()

    def __str__(self):
        return "%s - %s" % (self.interesado, self.turno)


class RetiroEntregaAnimal(models.Model):
    observaciones = models.TextField(max_length=200, default='', blank=True)
    baja = models.BooleanField(default=False)
    interesado = models.OneToOneField(m.PersonaGenerica, on_delete=models.CASCADE)
    mascota = models.OneToOneField('Mascota', on_delete=models.SET_NULL, null=True, blank=True)
    # baja logica, se hace sobre la mascota

    def __str__(self):
        return "%s" % self.interesado


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
    fecha = models.DateField(default=now)
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    mascota = models.OneToOneField('Mascota', on_delete=models.CASCADE)
    observaciones = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):
        return "%s %s" % (self.fecha, self.persona)


class Beneficio(models.Model):
    patente = models.ForeignKey('Patente', on_delete=models.CASCADE)
    fecha_antiparasitario = models.DateField()
    fecha_garrapaticida = models.DateField()
    observaciones = models.TextField(max_length=200, default='', blank=True)
