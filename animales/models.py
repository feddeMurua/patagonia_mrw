# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from personas import models as m
from .choices import *
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Analisis(models.Model):
    fecha = models.DateField(default=now)
    interesado = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE, related_name="interesado")
    procedencia = models.ForeignKey(m.Localidad, on_delete=models.CASCADE)
    toma_muestra = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE, related_name="toma_muestra", null=True)
    medico_veterinario = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE, null=True, blank=True,
                                           related_name="medico_veterinario")
    resultado = models.CharField(max_length=15, choices=Resultados, null=True)
    categoria = models.CharField(max_length=15, choices=Categorias)

    def __str__(self):
        return "Analisis n°: %s - %s" % (self.pk, self.fecha)


class Porcino(models.Model):
    precinto = models.IntegerField(unique=True)
    precinto2 = models.IntegerField(unique=True, blank=True, null=True)
    categoria_porcino = models.CharField(max_length=6, choices=Categoria_Porcino, default='LECHON')
    analisis = models.ForeignKey('Analisis', on_delete=models.CASCADE)

    def clean(self):
        porcinos = Porcino.objects.all()
        precintos1 = porcinos.values_list('precinto', flat=True)
        precintos2 = porcinos.values_list('precinto2', flat=True)
        if self.precinto in precintos2:
            raise ValidationError({'precinto': _('Ya existe un Porcino con este Precinto')}, code='unique')
        if self.precinto2 and self.precinto2 in precintos1:
            raise ValidationError({'precinto2': _('Ya existe un Porcino con este Precinto')}, code='unique')

    def __str__(self):
        return "%s - %s" % (self.categoria_porcino, self.precinto)

    def to_json(self):
        return {
            'categoria_porcino': self.categoria_porcino,
            'precinto': self.precinto,
            'precinto2': self.precinto2
        }


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
    anticonceptivos = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    partos = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    ultimo_celo = models.DateField(null=True, blank=True)
    turno = models.DateTimeField()

    def __str__(self):
        return "%s" % self.interesado


class RetiroEntregaAnimal(models.Model):
    fecha = models.DateField(default=now)
    interesado = models.ForeignKey(m.PersonaGenerica, on_delete=models.CASCADE)
    patentado = models.BooleanField(default=False)
    mascota = models.ForeignKey('Mascota', null=True)
    patente = models.IntegerField(null=True, blank=True)
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
    esterilizado = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.nombre, self.categoria_mascota)


class Patente(models.Model):
    nro_patente = models.BigIntegerField(validators=[MinValueValidator(0)])
    fecha = models.DateField(default=now)
    fecha_vencimiento = models.DateField()
    persona = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    mascota = models.ForeignKey('Mascota', on_delete=models.CASCADE)
    fecha_garrapaticida = models.DateField(null=True, blank=True)
    fecha_antiparasitario = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):
        return "Chapa: %s - %s" % (self.nro_patente, self.persona)
