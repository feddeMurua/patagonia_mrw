from personas import models as p
from libreta_curso import models as lc
import factory.fuzzy
import datetime


class CursoFactory(factory.django.DjangoModelFactory):
    fecha = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    cupo = factory.fuzzy.FuzzyInteger(0)
    lugar = factory.fuzzy.FuzzyText(length=25)
    finalizado = False

    class Meta:
        model = lc.Curso


class NacionalidadFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)

    class Meta:
        model = p.Nacionalidad


class ProvinciaFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)
    nacionalidad = factory.Iterator(p.Nacionalidad.objects.all())

    class Meta:
        model = p.Provincia


class LocalidadFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)
    cp = factory.fuzzy.FuzzyInteger(9000)
    provincia = factory.Iterator(p.Provincia.objects.all())

    class Meta:
        model = p.Localidad


class DomicilioFactory(factory.django.DjangoModelFactory):
    barrio = factory.fuzzy.FuzzyText(length=20)
    calle = factory.fuzzy.FuzzyText(length=50)
    calle_entre1 = factory.fuzzy.FuzzyText(length=50)
    calle_entre2 = factory.fuzzy.FuzzyText(length=50)
    nro = factory.fuzzy.FuzzyInteger(0)
    dpto = factory.fuzzy.FuzzyText(length=50)
    piso = factory.fuzzy.FuzzyInteger(0)
    localidad = factory.Iterator(p.Localidad.objects.all())

    class Meta:
        model = p.Domicilio


class PersonaFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)
    domicilio = DomicilioFactory()
    telefono = factory.fuzzy.FuzzyText(length=10)
    email = factory.fuzzy.FuzzyText(length=10)
    apellido = factory.fuzzy.FuzzyText(length=20)
    fecha_nacimiento = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    dni = factory.fuzzy.FuzzyText(length=25)
    nacionalidad = factory.Iterator(p.Nacionalidad.objects.all())
    obra_social = factory.fuzzy.FuzzyText(length=10)
    documentacion_retirada = False
    rubro = factory.fuzzy.FuzzyText(length=10)

    class Meta:
        model = p.PersonaFisica


class InscripcionFactory(factory.django.DjangoModelFactory):
    fecha_inscripcion = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    modificado = False
    calificacion = factory.fuzzy.FuzzyChoice(['Aprobado', 'Desaprobado', 'Sin Calificar'])
    porcentaje_asistencia = factory.fuzzy.FuzzyFloat(0.0)
    observaciones = factory.fuzzy.FuzzyText(length=25)
    curso = factory.Iterator(lc.Curso.objects.all())
    persona = factory.Iterator(p.PersonaFisica.objects.all())

    class Meta:
        model = lc.Inscripcion


class LibretaFactory(factory.django.DjangoModelFactory):
    persona = factory.Iterator(p.PersonaFisica.objects.all())
    curso = factory.Iterator(lc.Curso.objects.all())
    observaciones = factory.fuzzy.FuzzyText(length=25)
    fecha_examen_clinico = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    profesional_examen_clinico = factory.fuzzy.FuzzyText(length=25)
    lugar_examen_clinico = factory.fuzzy.FuzzyText(length=25)
    fecha = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    tipo_libreta = factory.fuzzy.FuzzyChoice(['Blanca', 'Amarilla', 'Celeste'])
    fecha_vencimiento = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))

    class Meta:
        model = lc.LibretaSanitaria


'''
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
'''
