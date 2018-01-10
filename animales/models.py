# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from personas import models as m
from .choices import *
from django.core.validators import MinValueValidator


class Analisis(models.Model):
    fecha = models.DateField(default=now)
    interesado = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE, related_name="interesado")
    procedencia = models.ForeignKey(m.Localidad, on_delete=models.CASCADE)
    medico_veterinario = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE,
                                           related_name="medico_veterinario")
    resultado = models.CharField(max_length=15, choices=Resultados)
    categoria = models.CharField(max_length=15, choices=Categorias)

    def __str__(self):
        return "Analisis n°: %s - %s" % (self.pk, self.fecha)


class Porcino(models.Model):
    precinto = models.BigIntegerField(unique=True)
    categoria_porcino = models.CharField(max_length=6, choices=Categoria_Porcino)
    analisis = models.ForeignKey('Analisis', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.categoria_porcino, self.precinto)


class ControlAntirrabico(models.Model):
    fecha_suceso = models.DateField(default=now)
    mordido = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE, related_name="mordido")
    responsable = models.ForeignKey(m.PersonaFisica, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="responsable")
    observaciones = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):
        return "%s - %s" % (self.fecha_suceso, self.mordido)


class Visita(models.Model):
    fecha_visita = models.DateField(default=now)
    control = models.ForeignKey('ControlAntirrabico')
    observaciones = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "%s" % self.fecha_visita


class SolicitudCriaderoCerdos(models.Model):
    fecha_solicitud = models.DateField(default=now)
    interesado = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    categoria_criadero = models.CharField(max_length=50, choices=Categoria_Criadero)
    domicilio_criadero = models.ForeignKey(m.DomicilioRural)
    observaciones = models.TextField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=10, default='En curso')

    def __str__(self):
        return "%s - %s" % (self.fecha_solicitud, self.interesado)


class DisposicionCriaderoCerdos(models.Model):
    fecha_disposicion = models.DateField()
    nro_disposicion = models.BigIntegerField()
    solicitud = models.OneToOneField('SolicitudCriaderoCerdos', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.fecha_disposicion, self.nro_disposicion)


class AplazoSolicitud(models.Model):
    fecha_aplazo = models.DateField(default=now)
    motivo_aplazo = models.TextField(max_length=200)
    solicitud = models.ForeignKey('SolicitudCriaderoCerdos', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.fecha_aplazo, self.motivo_aplazo)


class Esterilizacion(models.Model):
    interesado = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)
    mascota = models.ForeignKey('Mascota', on_delete=models.SET_NULL, null=True)
    anticonceptivos = models.IntegerField(validators=[MinValueValidator(0)], blank=True)
    partos = models.IntegerField(validators=[MinValueValidator(0)], blank=True)
    ultimo_celo = models.DateField(blank=True)
    turno = models.DateTimeField()

    def __str__(self):
        return "%s" % self.interesado


'''
class Turno(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_hora = models.DateTimeField()
    esterilizacion = models.ForeignKey('Esterilizacion', on_delete=models.CASCADE)
'''


class RetiroEntregaAnimal(models.Model):
    fecha = models.DateField(default=now)
    interesado = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)
    patentado = models.BooleanField(default=False)
    mascota = models.ForeignKey('Mascota', null=True)
    tramite = models.CharField(max_length=10, choices=Tramites)
    observaciones = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):
        return "%s" % self.interesado

    def to_json(self):
        return {'tramite': self.tramite, 'observaciones': self.observaciones, 'patentado': self.patentado}


class Mascota(models.Model):
    nombre = models.CharField(max_length=50)
    pelaje = models.CharField(max_length=50)
    categoria_mascota = models.CharField(max_length=6, choices=Categoria_Mascota)
    raza = models.CharField(max_length=50)
    sexo = models.CharField(max_length=15, choices=Sexo)
    nacimiento_fecha = models.DateField(blank=True, null=True)
    baja = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s - %s" % (self.nombre, self.raza, self.pelaje)


class Patente(models.Model):
    fecha_vencimiento = models.DateField()
    persona = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    mascota = models.ForeignKey('Mascota', on_delete=models.CASCADE)
    fecha_garrapaticida = models.DateField(null=True)
    fecha_antiparasitario = models.DateField(null=True)
    observaciones = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):
        return "Chapa: %s - %s" % (self.pk, self.persona)
