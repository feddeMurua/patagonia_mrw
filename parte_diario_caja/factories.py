from .models import *
from personas import models as m
import factory
import factory.fuzzy
import datetime

'''
MOVER DIRECCION, LOCALIDAD, PROVINCIA, NACIONALIDAD,
A FACTORY EN PERSONAS
'''

class NacionalidadFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)

    class Meta:
        model = m.Nacionalidad


class ProvinciaFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)
    nacionalidad = NacionalidadFactory()

    class Meta:
        model = m.Provincia


class LocalidadFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)
    cp = factory.fuzzy.FuzzyInteger(9000)
    provincia = ProvinciaFactory()

    class Meta:
        model = m.Localidad


class DomicilioFactory(factory.django.DjangoModelFactory):
    barrio = factory.fuzzy.FuzzyText(length=20)
    calle = factory.fuzzy.FuzzyText(length=50)
    calle_entre1 = factory.fuzzy.FuzzyText(length=50)
    calle_entre2 = factory.fuzzy.FuzzyText(length=50)
    nro = factory.fuzzy.FuzzyInteger(0)
    dpto = factory.fuzzy.FuzzyText(length=50)
    piso = factory.fuzzy.FuzzyInteger(0)
    localidad = LocalidadFactory()

    class Meta:
        model = m.Domicilio


class TipoServicioFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=50)

    class Meta:
        model = TipoServicio


class ServicioFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=50)
    importe = factory.fuzzy.FuzzyFloat(0.0)
    tipo = TipoServicio.objects.create(nombre=factory.fuzzy.FuzzyText(length=50))

    class Meta:
        model = Servicio


class MovimientoDiarioFactory(factory.django.DjangoModelFactory):
    fecha = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    nro_ingreso = factory.fuzzy.FuzzyInteger(1000)

    class Meta:
        model = MovimientoDiario


class DetalleMovimientoFactory(factory.django.DjangoModelFactory):
    movimiento = MovimientoDiarioFactory()
    servicio = ServicioFactory()
    descripcion = factory.fuzzy.FuzzyText(length=50)
    titular = m .PersonaGenerica.objects.create(
                                        nombre=factory.fuzzy.FuzzyText(length=50),
                                        domicilio=DomicilioFactory(),
                                        telefono=factory.fuzzy.FuzzyText(length=50),
                                        email="un_email@dominio.com"
                                        )
    forma_pago = factory.fuzzy.FuzzyChoice(choices=TipoPago)
    nro_cheque = factory.fuzzy.FuzzyText(length=50)

    class Meta:
        model = DetalleMovimiento
