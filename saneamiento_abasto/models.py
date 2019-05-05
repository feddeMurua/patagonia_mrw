# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from solo.models import SingletonModel
from parte_diario_caja import models as pd_m
from personas import models as m
from .choices import *


class Abastecedor(models.Model):
    responsable = models.OneToOneField(m.PersonaGenerica, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Abastecedor, self).save(*args, **kwargs)
        CuentaCorriente.objects.create(abastecedor=self)

    def __str__(self):
        return "%s" % self.responsable


class ReinspeccionProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    kilo_producto = models.FloatField()
    reinspeccion = models.ForeignKey('Reinspeccion', on_delete=models.CASCADE)

    def __str__(self):
        return "%s || %s" % (self.producto.nombre, self.reinspeccion)

    def to_json(self):
        return {
            'producto': {'nombre': self.producto.nombre},
            'kilo_producto': self.kilo_producto
        }


class Producto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return "%s" % self.nombre

    def to_json(self):
        return {'nombre': self.nombre}


class Reinspeccion(models.Model):
    fecha = models.DateField(default=now)
    turno = models.CharField(max_length=10, choices=TURNO_REINSPECCION)
    inspectores = models.ManyToManyField(m.PersonalPropio)
    precintado = models.IntegerField(null=True, blank=True)
    certificado = models.CharField(max_length=15, unique=True)
    abastecedor = models.ForeignKey('Abastecedor', on_delete=models.CASCADE)
    total_kg = models.IntegerField(validators=[MinValueValidator(1)])
    importe = models.FloatField(null=True, blank=True)
    detalles = models.BooleanField(default=True)
    origen = models.ForeignKey(m.Localidad, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.abastecedor)


class ReinspeccionPrecios(SingletonModel):
    kg_min = models.IntegerField(validators=[MinValueValidator(1)], default=30)
    precio_min = models.FloatField(validators=[MinValueValidator(0)], default=55)
    precio_kg = models.FloatField(validators=[MinValueValidator(0)], default=0.25)

    def __unicode__(self):
        return u"Precios Vigentes Reinspeccion"

    class Meta:
        verbose_name = "Precios Vigentes Reinspeccion"


'''
CUENTAS CORRIENTES
'''


class CuentaCorriente(models.Model):
    abastecedor = models.OneToOneField('Abastecedor', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Cuenta: %s - %s" % (self.pk, self.abastecedor)


class PeriodoCC(models.Model):
    cc = models.ForeignKey('CuentaCorriente', on_delete=models.CASCADE, null=True)
    periodo = models.DateField(blank=True, null=True)
    total_kg = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    importe = models.FloatField(validators=[MinValueValidator(0)], default=0)
    fecha_certificado = models.DateField(blank=True, null=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return "%s-%s / %s" % (self.periodo.month, self.periodo.year, self.cc)


class DetalleCC(models.Model):
    reinspeccion = models.ForeignKey('Reinspeccion', on_delete=models.CASCADE)
    periodo = models.ForeignKey('PeriodoCC', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "%s" % self.reinspeccion

    def save(self, *args, **kwargs):
        try:
            periodo = PeriodoCC.objects.get(periodo__month=self.reinspeccion.fecha.month,
                                            periodo__year=self.reinspeccion.fecha.year,
                                            cc=CuentaCorriente.objects.get(abastecedor=self.reinspeccion.abastecedor))
            periodo.total_kg += self.reinspeccion.total_kg
            periodo.importe += self.reinspeccion.importe
        except:
            periodo = PeriodoCC.objects.create(periodo=self.reinspeccion.fecha, importe=self.reinspeccion.importe,
                                               total_kg=self.reinspeccion.total_kg,
                                               cc=CuentaCorriente.objects.get(abastecedor=self.reinspeccion.abastecedor))
        periodo.save()
        self.periodo = periodo
        super(DetalleCC, self).save(*args, **kwargs)


'''
VEHICULO Y DESINFECCIONES
'''


class Vehiculo(models.Model):
    modelo = models.ForeignKey('ModeloVehiculo')
    anio = models.IntegerField(validators=[MinValueValidator(1950)], blank=True, null=True)
    dominio = models.CharField(max_length=50, unique=True)
    titular = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE)
    tipo_vehiculo = models.CharField(max_length=3, choices=TIPO_VEHICULO, default='TPP')
    nro = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
    tipo_tpp = models.CharField(max_length=15, blank=True, null=True, choices=TIPO_TPP)
    disposicion_resolucion = models.CharField(max_length=50, blank=True, null=True, unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA, blank=True, null=True)
    rubro_vehiculo = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "%s %s - %s" % (self.modelo.nombre, self.modelo.marca, self.dominio)


class MarcaVehiculo(models.Model):
    nombre = models.CharField(max_length=15)

    def __str__(self):
        return "%s" % self.nombre


class ModeloVehiculo(models.Model):
    nombre = models.CharField(max_length=15)
    marca = models.ForeignKey('MarcaVehiculo')

    def __str__(self):
        return "%s %s" % (self.marca, self.nombre)


class Desinfeccion(models.Model):
    fecha_realizacion = models.DateField(default=now)
    proximo_vencimiento = models.DateField()
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)
    quincena = models.CharField(max_length=30)
    justificativo = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_realizacion, self.vehiculo, self.vehiculo.titular)


class ControlDePlaga(models.Model):
    fecha = models.DateField(default=now)
    responsable = models.ForeignKey(m.PersonaFisica, on_delete=models.CASCADE, related_name="responsable_propietario")
    funcionario_actuante = models.ForeignKey(m.PersonalPropio, on_delete=models.CASCADE, related_name="funcionario")
    tipo_plaga = models.CharField(max_length=50, choices=PLAGAS)
    procedimiento = models.CharField(max_length=400)
    recomendaciones = models.CharField(max_length=400, blank=True, null=True)
    pagado = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha, self.responsable, self.tipo_plaga)


class VisitaControl(models.Model):
    fecha = models.DateField()
    observaciones = models.TextField(max_length=200, null=True, blank=True)
    control = models.ForeignKey('ControlDePlaga', on_delete=models.CASCADE)
    realizada = models.BooleanField(default=False)

    def __str__(self):
        return "Control N°:%s - %s" % (self.control.pk, self.fecha)


class PagoDiferido(models.Model):
    monto = models.FloatField()
    fecha_pago = models.CharField(max_length=15, choices=PAGO_DIFERIDO)
    control = models.ForeignKey('ControlDePlaga', on_delete=models.CASCADE)

    def detalles(self, nombre_servicio, control):
        servicio = pd_m.Servicio.objects.get(nombre=nombre_servicio)
        self.monto = servicio.importe
        self.control = control
        self.save()

    def __str__(self):
        return "%s - %s - %s" % (self.control.responsable, self.control.tipo_plaga, self.fecha_pago)
