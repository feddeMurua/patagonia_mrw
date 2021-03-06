from personas import models as p
from libreta_curso import models as lc
from animales import models as a
from saneamiento_abasto import models as sa
import factory.fuzzy
import datetime


'''
#Para cargar con el factory

for x in xrange(10):
    cursos = factories.CursoFactory()

for x in xrange(45):
    personas = factories.PersonaFactory()

for x in xrange(45):
    inscripciones = factories.InscripcionFactory()

for x in xrange(45):
    libretas = factories.LibretaFactory()

for x in xrange(45):
    vehiculos = factories.VehiculoFactory()

for x in xrange(85):
    desinfecciones = factories.DesinfeccionFactory()

for x in xrange(50):
    mascotas = factories.MascotaFactory()

for x in xrange(50):
    patentes = factories.PatenteFactory()

for x in xrange(50):
    esterilizacion = factories.EsterilizacionFactory()

for x in xrange(50):
    retiro_entrega = factories.RetiroEntregaAnimalFactory()

for x in xrange(50):
    analisis = factories.AnalisisFactory()


class DesinfeccionFactory(factory.django.DjangoModelFactory):
    fecha_realizacion = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    proximo_vencimiento = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    vehiculo = factory.Iterator(sa.Vehiculo.objects.all())
    quincena = factory.fuzzy.FuzzyChoice(['Primera', 'Segunda'])
    infraccion = False

    class Meta:
        model = sa.Desinfeccion


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
    fecha_inscripcion = '2018-01-28'
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
    #fecha = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    fecha = '2018-01-31'
    tipo_libreta = factory.fuzzy.FuzzyChoice(['Blanca', 'Amarilla', 'Celeste'])
    fecha_vencimiento = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))

    class Meta:
        model = lc.LibretaSanitaria


class AnalisisFactory(factory.django.DjangoModelFactory):
    fecha = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    interesado = factory.Iterator(p.PersonaFisica.objects.all())
    procedencia = factory.Iterator(p.Localidad.objects.all())
    medico_veterinario = factory.Iterator(p.PersonalPropio.objects.all())
    resultado = factory.fuzzy.FuzzyChoice(['Positivo','Negativo'])
    categoria = factory.fuzzy.FuzzyChoice(['Lechon','Porker','Adulto'])

    class Meta:
        model = a.Analisis


class MascotaFactory(factory.django.DjangoModelFactory):
    nombre = factory.fuzzy.FuzzyText(length=25)
    pelaje = factory.fuzzy.FuzzyText(length=25)
    categoria_mascota = factory.fuzzy.FuzzyChoice(['CANINA','FELINA'])
    raza = factory.fuzzy.FuzzyText(length=25)
    sexo = factory.fuzzy.FuzzyChoice(['Macho','Hembra'])
    baja = False

    class Meta:
        model = a.Mascota


class PatenteFactory(factory.django.DjangoModelFactory):
    fecha = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    fecha_vencimiento = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    persona = factory.Iterator(p.PersonaFisica.objects.all())
    mascota = factory.Iterator(a.Mascota.objects.all())
    fecha_garrapaticida = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    fecha_antiparasitario = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    observaciones = factory.fuzzy.FuzzyText(length=25)

    class Meta:
        model = a.Patente


class EsterilizacionFactory(factory.django.DjangoModelFactory):
    interesado = factory.Iterator(p.PersonaGenerica.objects.all())
    mascota = factory.Iterator(a.Mascota.objects.all())
    anticonceptivos = factory.fuzzy.FuzzyInteger(0)
    partos = factory.fuzzy.FuzzyInteger(0)
    ultimo_celo = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))
    turno = factory.fuzzy.FuzzyDate(datetime.date(2000, 1, 1))

    class Meta:
        model = a.Esterilizacion


class RetiroEntregaAnimalFactory(factory.django.DjangoModelFactory):
    interesado = factory.Iterator(p.PersonaGenerica.objects.all())
    patentado = False
    mascota = factory.Iterator(a.Mascota.objects.all())
    tramite = factory.fuzzy.FuzzyChoice(['ENTREGA','RETIRO'])
    observaciones = factory.fuzzy.FuzzyText(length=25)

    class Meta:
        model = a.RetiroEntregaAnimal



class VehiculoFactory(factory.django.DjangoModelFactory):
    marca = factory.fuzzy.FuzzyChoice(['Chevrolet', 'Fiat', 'Ford', 'Renault'])
    dominio = factory.fuzzy.FuzzyText(length=5)
    titular = factory.Iterator(p.PersonaFisica.objects.all())
    tipo_vehiculo = factory.fuzzy.FuzzyChoice(['TSA', 'TPP'])
    tipo_tpp = factory.fuzzy.FuzzyChoice(['Colectivo', 'TR','Escolar'])
    categoria = factory.fuzzy.FuzzyChoice(['Categoria_A', 'Categoria_B', 'Categoria_C' ,'Categoria_D', 'Categoria_E'])

    class Meta:
        model = sa.Vehiculo


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
