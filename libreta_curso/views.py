# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from easy_pdf.views import PDFTemplateView
from .forms import *
from .models import *
from desarrollo_patagonia.utils import *
from parte_diario_caja import forms as pd_f
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from dateutil.relativedelta import *
from django.utils import timezone
import json
import numpy as np
from desarrollo_patagonia import factories
import collections
import datetime

#Para mover a las views correspondientes
from animales import models as a_models

'''
CURSOS
'''


@login_required(login_url='login')
def lista_curso(request):
    return render(request, 'curso/curso_list.html', {'fecha_hoy': timezone.now().date(), 'listado': Curso.objects.all()})


@login_required(login_url='login')
def alta_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Curso de Manipulacion de Alimentos')
            return redirect('cursos:lista_cursos')
    else:
        form = CursoForm
    return render(request, 'curso/curso_form.html', {'form': form})


@staff_member_required
@login_required(login_url='login')
def baja_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    log_eliminar(request.user.id, curso, 'Curso de Manipulacion de Alimentos')
    curso.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Curso de Manipulacion de Alimentos')
            return redirect('cursos:lista_cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'curso/curso_form.html', {'form': form})


@login_required(login_url='login')
def cierre_de_curso(request, id_curso):
    if request.method == 'POST':
        curso = Curso.objects.get(pk=id_curso)
        curso.finalizado = True
        curso.save()
        log_modificar(request.user.id, curso, 'Cierre de Curso')
        return redirect('cursos:lista_cursos')
    else:
        lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
        apto_cierre = True
        for inscripcion in lista_inscripciones:
            if not inscripcion.modificado:
                apto_cierre = False
                break
        return render(request, "curso/curso_cierre.html", {'id_curso': id_curso, 'listado': lista_inscripciones,
                                                           'apto_cierre': apto_cierre})


class PdfAsistencia(LoginRequiredMixin, PDFTemplateView):
    template_name = 'curso/asistencia_pdf.html'
    title = "Planilla de Asistencia de Alumnos"

    def get_context_data(self, pk):  # pk del curso por paŕametro
        lista_inscripciones = Inscripcion.objects.filter(curso__pk=pk)
        curso = Curso.objects.get(id=pk)
        return super(PdfAsistencia, self).get_context_data(
            lista_inscripciones=lista_inscripciones,
            curso=curso,
            title="Curso"
        )


class PdfAprobados(LoginRequiredMixin, PDFTemplateView):
    template_name = 'curso/aprobados_pdf.html'
    title = "Planilla de Alumnos Aprobados"

    def get_context_data(self, pk):  # pk del curso por paŕametro
        lista_inscripciones = Inscripcion.objects.filter(curso__pk=pk, calificacion="Aprobado")
        curso = Curso.objects.get(id=pk)
        return super(PdfAprobados, self).get_context_data(
            lista_inscripciones=lista_inscripciones,
            curso=curso,
            title="Curso"
        )


'''
INSCRIPCIONES
'''


@login_required(login_url='login')
def lista_inscripciones_curso(request, id_curso):
    lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
    curso = Curso.objects.get(pk=id_curso)
    cupo_restante = curso.cupo - len(lista_inscripciones)
    return render(request, "curso/curso_inscripciones.html", {'fecha_hoy': timezone.now().date(), 'curso': curso,
                                                              'cupo_restante': cupo_restante,
                                                              'listado': lista_inscripciones})


@login_required(login_url='login')
def alta_inscripcion(request, id_curso):
    if request.method == 'POST':
        form = InscripcionForm(request.POST, id_curso=id_curso)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.curso = Curso.objects.get(pk=id_curso)
            inscripcion.save()
            log_crear(request.user.id, inscripcion, 'Inscripcion a Curso')
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', args=id_curso))
    else:
        form = InscripcionForm
    url_return = 'cursos:inscripciones_curso'
    return render(request, "inscripcion/inscripcion_form.html", {'id_curso': id_curso, 'url_return': url_return,
                                                                 'form': form})


@login_required(login_url='login')
def baja_inscripcion(request, pk):
    inscripcion = Inscripcion.objects.get(pk=pk)
    log_eliminar(request.user.id, inscripcion, 'Inscripcion a Curso')
    inscripcion.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_inscripcion(request, pk, id_curso):
    inscripcion = Inscripcion.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionInscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Inscripcion a Curso')
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', kwargs={'id_curso': id_curso}))
    else:
        form = ModificacionInscripcionForm(instance=inscripcion)
    return render(request, 'inscripcion/inscripcion_form.html', {'form': form, 'id_curso': id_curso,
                                                                 'url_return': 'cursos:inscripciones_curso',
                                                                 'modificacion': True})


@login_required(login_url='login')
def cierre_inscripcion(request, pk, id_curso):
    inscripcion = Inscripcion.objects.get(pk=pk)
    if request.method == 'POST':
        form = CierreInscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            form.save()
            inscripcion.modificado = True
            inscripcion.save()
            log_modificar(request.user.id, inscripcion, 'Calificacion de Inscripcion en Curso')
            return HttpResponseRedirect(reverse('cursos:cierre_curso', kwargs={'id_curso': id_curso}))
    else:
        form = CierreInscripcionForm(instance=inscripcion)
    return render(request, 'inscripcion/inscripcion_form.html', {'form': form, 'id_curso': id_curso,
                                                                 'url_return': 'cursos:cierre_curso',
                                                                 'modificacion': True})


class PdfInscripcion(LoginRequiredMixin, PDFTemplateView):
    template_name = 'inscripcion/inscripcion_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        inscripcion = Inscripcion.objects.get(pk=pk)
        return super(PdfInscripcion, self).get_context_data(
            pagesize="A4",
            inscripcion=inscripcion
        )


'''
LIBRETRAS SANITARIAS
'''


def get_cursos(pk_persona):
    inscripciones = Inscripcion.objects.filter(persona__pk=pk_persona)
    cursos = []
    for inscripcion in inscripciones:
        if inscripcion.calificacion == 'Aprobado':
            cursos.append(inscripcion.curso)
    return cursos


@login_required(login_url='login')
def lista_libreta(request):
    return render(request, 'libreta/libreta_list.html', {'listado': LibretaSanitaria.objects.all(),
                                                         'fecha_hoy': timezone.now()})


@login_required(login_url='login')
def alta_libreta(request):
    if request.method == 'POST':
        form = LibretaForm(request.POST, request.FILES)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        servicio_form = pd_f.ListaServicios(request.POST, tipo='Libreta Sanitaria')
        if form.is_valid() & detalle_mov_form.is_valid() & servicio_form.is_valid():
            libreta = form.save(commit=False)
            if libreta.tipo_libreta != 'Celeste':
                libreta.fecha_vencimiento = timezone.now().date() + relativedelta(years=1)
            else:
                libreta.fecha_vencimiento = timezone.now().date() + relativedelta(months=int(request.POST['meses']))
            cursos = get_cursos(libreta.persona.pk)
            if cursos:
                libreta.curso = cursos[-1]
            libreta.save()
            detalle_mov = detalle_mov_form.save(commit=False)
            detalle_mov.completar(servicio_form.cleaned_data['servicio'], libreta)
            log_crear(request.user.id, libreta, 'Libreta Sanitaria')
            return redirect('libretas:lista_libretas')
    else:
        form = LibretaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        servicio_form = pd_f.ListaServicios(tipo='Libreta Sanitaria')
    return render(request, 'libreta/libreta_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                         'servicio_form': servicio_form})


class DetalleLibreta(LoginRequiredMixin, DetailView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@staff_member_required
@login_required(login_url='login')
def baja_libreta(request, pk):
    libreta = LibretaSanitaria.objects.get(pk=pk)
    log_eliminar(request.user.id, libreta, 'Libreta Sanitaria')
    libreta.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_libreta(request, pk):
    libreta = LibretaSanitaria.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionLibretaForm(request.POST, instance=libreta)
        if form.is_valid():
            libreta = form.save(commit=False)
            if libreta.tipo_libreta != 'Celeste':
                libreta.fecha_vencimiento = timezone.now().date() + relativedelta(years=1)
            else:
                libreta.fecha_vencimiento = timezone.now().date() + relativedelta(months=int(request.POST['meses']))
                libreta.save()
            log_modificar(request.user.id, libreta, 'Libreta Sanitaria')
            return redirect('libretas:lista_libretas')
    else:
        form = ModificacionLibretaForm(instance=libreta)
    return render(request, 'libreta/libreta_form.html', {'form': form, 'modificacion': True})


class PdfLibreta(LoginRequiredMixin, PDFTemplateView):
    template_name = 'libreta/libreta_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        libreta = LibretaSanitaria.objects.get(pk=pk)
        return super(PdfLibreta, self).get_context_data(
            pagesize="A4",
            libreta=libreta
        )


'''
ESTADÍSTICAS
'''


@login_required(login_url='login')
def opciones_estadisticas(request):

    '''
    # PARA FILTRAR POR DATE RANGE MAS ADELANTE
    if request.method == 'POST':

        fecha_desde = datetime.datetime.strptime(request.POST.get('desde'), '%d/%m/%Y').strftime('%Y-%m-%d')
        fecha_hasta = datetime.datetime.strptime(request.POST.get('hasta'), '%d/%m/%Y').strftime('%Y-%m-%d')

        return redirect('cursos:opciones_estadisticas')
    '''

    # CALIFICACIONES

    # diccionario de datos
    aprobados_curso = {}
    desaprobados_curso = {}
    s_c_curso = {}

    years = Curso.objects.values_list('fecha')

    for anio in years:

        # acumuladores
        s_c = 0
        aprobados = 0
        desaprobados = 0

        cursos_anio = Inscripcion.objects.filter(curso__fecha__year=anio[0].year).values_list("calificacion")

        for nota in cursos_anio:
            if nota[0] == "Sin Calificar":
                s_c += 1
            elif nota[0] == "Aprobado":
                aprobados += 1
            else:
                desaprobados += 1

        s_c_curso[str(anio[0].year)] = s_c
        aprobados_curso[str(anio[0].year)] = aprobados
        desaprobados_curso[str(anio[0].year)] = desaprobados


    ord_s_c_curso = collections.OrderedDict(sorted(s_c_curso.items()))
    ord_aprobados = collections.OrderedDict(sorted(aprobados_curso.items()))
    ord_desaprobados = collections.OrderedDict(sorted(desaprobados_curso.items()))

    label_curso_anios = ord_s_c_curso.keys()  # indistinto para los datos (tienen la misma clave)
    datos_sc = ord_s_c_curso.values()
    datos_aprobados = ord_aprobados.values()
    datos_desaprobados = ord_desaprobados.values()

    # CURSOS POR AÑO

    cursos_anuales = {}

    years = Curso.objects.values_list('fecha')

    for anio in years:
            cursos_anuales[str(anio[0].year)] = Curso.objects.filter(fecha__year=anio[0].year).count()

    ord_cursos_anuales = collections.OrderedDict(sorted(cursos_anuales.items()))

    label_year = ord_cursos_anuales.keys()
    datos_cursos_anuales = ord_cursos_anuales.values()

    # INSCRIPCIONES A CURSO

    inscripciones = {}  # inscripciones por curso

    cursos = Curso.objects.all()

    for curso in cursos:
        inscripciones[str(curso.fecha)] = Inscripcion.objects.filter(curso__fecha=curso.fecha).count()

    ord_inscripciones = collections.OrderedDict(sorted(inscripciones.items()))

    label_cursos = ord_inscripciones.keys()
    datos_inscripciones = ord_inscripciones.values()

    # LIBRETAS POR TIPO

    # diccionario de datos
    libretas_blancas = {}
    libretas_amarillas = {}
    libretas_celestes = {}

    years = LibretaSanitaria.objects.values_list('fecha')

    for anio in years:

        # acumuladores
        blancas = 0
        amarillas = 0
        celestes = 0

        libretras_anio = LibretaSanitaria.objects.filter(fecha__year=anio[0].year).values_list("tipo_libreta")

        for color in libretras_anio:
            if color[0] == "Blanca":
                blancas += 1
            elif color[0] == "Amarilla":
                amarillas += 1
            else:
                celestes += 1

        libretas_blancas[str(anio[0].year)] = blancas
        libretas_amarillas[str(anio[0].year)] = amarillas
        libretas_celestes[str(anio[0].year)] = celestes


    ord_libretas_blancas = collections.OrderedDict(sorted(libretas_blancas.items()))
    ord_libretas_amarillas = collections.OrderedDict(sorted(libretas_amarillas.items()))
    ord_libretas_celestes = collections.OrderedDict(sorted(libretas_celestes.items()))

    label_libretas_anios = ord_libretas_blancas.keys() # indistinto para los datos (tienen la misma clave)
    datos_blanca = ord_libretas_blancas.values()
    datos_amarilla = ord_libretas_amarillas.values()
    datos_celeste = ord_libretas_celestes.values()


    '''
    ------------------------------------
    '''

    #Analisis

    todos_analisis = {}

    analisis = a_models.Analisis.objects.all()

    years = a_models.Analisis.objects.values_list('fecha')

    for anio in years:
            todos_analisis[str(anio[0].year)] = a_models.Analisis.objects.filter(fecha__year=anio[0].year).count()

    ord_analisis = collections.OrderedDict(sorted(todos_analisis.items()))

    label_analisis = ord_analisis.keys()
    datos_analisis = ord_analisis.values()

    #Categorías análisis

    porker_analisis = {}
    lechon_analisis = {}
    adulto_analisis = {}

    years = a_models.Analisis.objects.values_list('fecha')

    for anio in years:

        #acumuladores
        porker = 0
        lechon = 0
        adulto = 0

        categorias_analisis = a_models.Analisis.objects.filter(fecha__year=anio[0].year).values_list("categoria")

        for categoria in categorias_analisis:
            if categoria[0] == "Porker":
                porker+=1
            elif categoria[0] == "Lechon":
                lechon+=1
            else:
                adulto+=1

        porker_analisis[str(anio[0].year)] = porker
        lechon_analisis[str(anio[0].year)] = lechon
        adulto_analisis[str(anio[0].year)] = adulto


    ord_porker_analisis = collections.OrderedDict(sorted(porker_analisis.items()))
    ord_lechon_analisis = collections.OrderedDict(sorted(lechon_analisis.items()))
    ord_adulto_analisis = collections.OrderedDict(sorted(adulto_analisis.items()))

    label_categoria_analisis = ord_adulto_analisis.keys() # indistinto para los datos (tienen la misma clave)
    datos_porker = ord_porker_analisis.values()
    datos_lechon = ord_lechon_analisis.values()
    datos_adulto = ord_adulto_analisis.values()

    '''
    ------------------------------------
    '''
    #patentamiento

    patente_can_macho = {}
    patente_can_hembra = {}
    patente_fel_macho = {}
    patente_fel_hembra = {}

    years = a_models.Patente.objects.values_list('fecha')

    for anio in years:

        #acumuladores
        can_macho = 0
        can_hembra = 0
        fel_macho = 0
        fel_hembra = 0

        patentes_caninos = a_models.Patente.objects.filter(fecha__year=anio[0].year).values_list("mascota__categoria_mascota","mascota__sexo")

        for patente in patentes_caninos:
            if (patente[0] == 'CANINA') and (patente[1] == 'Macho'):
                can_macho+=1
            elif (patente[0] == 'CANINA') and (patente[1] == 'Hembra'):
                can_hembra+=1
            elif (patente[0] == 'FELINA') and (patente[1] == 'Macho'):
                fel_macho+=1
            else:
                fel_hembra+=1

        patente_can_macho[str(anio[0].year)] = can_macho
        patente_can_hembra[str(anio[0].year)] = can_hembra
        patente_fel_macho[str(anio[0].year)] = fel_macho
        patente_fel_hembra[str(anio[0].year)] = fel_hembra

    ord_patente_can_macho = collections.OrderedDict(sorted(patente_can_macho.items()))
    ord_patente_can_hembra = collections.OrderedDict(sorted(patente_can_hembra.items()))
    ord_patente_fel_macho = collections.OrderedDict(sorted(patente_fel_macho.items()))
    ord_patente_fel_hembra = collections.OrderedDict(sorted(patente_fel_hembra.items()))

    label_categoria_patente = ord_patente_can_macho.keys() # indistinto para los datos (tienen la misma clave)
    datos_can_macho = ord_patente_can_macho.values()
    datos_can_hembra = ord_patente_can_hembra.values()
    datos_fel_macho = ord_patente_fel_macho.values()
    datos_fel_hembra = ord_patente_fel_hembra.values()


    '''
    ------------------------------------
    '''


    '''
    ------------------------------------
    '''
    #esterilizacion

    esterilizacion_can_macho = {}
    esterilizacion_can_hembra = {}
    esterilizacion_fel_macho = {}
    esterilizacion_fel_hembra = {}

    years = a_models.Esterilizacion.objects.values_list('turno')

    for anio in years:

        #acumuladores
        can_macho = 0
        can_hembra = 0
        fel_macho = 0
        fel_hembra = 0

        esterilizaciones = a_models.Esterilizacion.objects.filter(turno__year=anio[0].year).values_list("mascota__categoria_mascota","mascota__sexo")

        for esterilizacion  in esterilizaciones:
            if (esterilizacion[0] == 'CANINA') and (esterilizacion[1] == 'Macho'):
                can_macho+=1
            elif (esterilizacion[0] == 'CANINA') and (esterilizacion[1] == 'Hembra'):
                can_hembra+=1
            elif (esterilizacion[0] == 'FELINA') and (esterilizacion[1] == 'Macho'):
                fel_macho+=1
            else:
                fel_hembra+=1

        esterilizacion_can_macho[str(anio[0].year)] = can_macho
        esterilizacion_can_hembra[str(anio[0].year)] = can_hembra
        esterilizacion_fel_macho[str(anio[0].year)] = fel_macho
        esterilizacion_fel_hembra[str(anio[0].year)] = fel_hembra

    ord_esterilizacion_can_macho = collections.OrderedDict(sorted(esterilizacion_can_macho.items()))
    ord_esterilizacion_can_hembra = collections.OrderedDict(sorted(esterilizacion_can_hembra.items()))
    ord_esterilizacion_fel_macho = collections.OrderedDict(sorted(esterilizacion_fel_macho.items()))
    ord_esterilizacion_fel_hembra = collections.OrderedDict(sorted(esterilizacion_fel_hembra.items()))

    label_categoria_esterilizacion = ord_esterilizacion_can_macho.keys() # indistinto para los datos (tienen la misma clave)
    datos_esterilizacion_can_macho = ord_esterilizacion_can_macho.values()
    datos_esterilizacion_can_hembra = ord_esterilizacion_can_hembra.values()
    datos_esterilizacion_fel_macho = ord_esterilizacion_fel_macho.values()
    datos_esterilizacion_fel_hembra = ord_esterilizacion_fel_hembra.values()


    '''
    ------------------------------------
    '''


    '''
    ------------------------------------
    '''

    #RETIRO Y ENTREGA DE ANIMALES

    #diccionario de datos
    entrega_animales = {}
    retiro_animales = {}

    years = a_models.RetiroEntregaAnimal.objects.values_list('fecha')

    for anio in years:

        #acumuladores
        entregas = 0
        retiros = 0


        animales_anio = a_models.RetiroEntregaAnimal.objects.filter(fecha__year=anio[0].year).values_list("tramite")

        for animal in animales_anio:
            if animal[0] == "ENTREGA":
                entregas+=1
            elif animal[0] == "RETIRO":
                retiros+=1


        entrega_animales[str(anio[0].year)] = entregas
        retiro_animales[str(anio[0].year)] = retiros



    ord_entrega_animales = collections.OrderedDict(sorted(entrega_animales.items()))
    ord_retiro_animales = collections.OrderedDict(sorted(retiro_animales.items()))


    label_animales_anios = ord_entrega_animales.keys() # indistinto para los datos (tienen la misma clave)
    datos_entrega = ord_entrega_animales.values()
    datos_retiro = ord_retiro_animales.values()

    print("------------------------------")
    print(a_models.RetiroEntregaAnimal.objects.filter(tramite='ENTREGA').count())
    print(a_models.RetiroEntregaAnimal.objects.filter(tramite='RETIRO').count())
    print("------------------------------")


    '''
    -----------------------------------
    '''


    '''
    CONTEXTO
    '''
    
    context = {
        # inscripciones
        'promedio_inscriptos': int(np.average(datos_inscripciones)),
        # cursos
        'promedio_anual': int(np.average(datos_cursos_anuales)),
        # calificaciones
        'promedio_sc': int(np.average(datos_sc)),
        'promedio_aprobados': int(np.average(datos_aprobados)),
        'promedio_desaprobados': int(np.average(datos_desaprobados)),
        # libretas
        'promedio_blanca': int(np.average(datos_blanca)),
        'promedio_amarilla': int(np.average(datos_amarilla)),
        'promedio_celeste': int(np.average(datos_celeste)),
        #analisis
        'promedio_analisis': int(np.average(datos_analisis)),
        'promedio_porkers': int(np.average(datos_porker)),
        'promedio_lechones': int(np.average(datos_lechon)),
        'promedio_adultos': int(np.average(datos_adulto)),
        #mascotas
        'promedio_can_macho': int(np.average(datos_can_macho)),
        'promedio_can_hembra': int(np.average(datos_can_hembra)),
        'promedio_fel_macho': int(np.average(datos_fel_macho)),
        'promedio_fel_hembra': int(np.average(datos_fel_hembra)),
        #esterilizacion
        'promedio_esterilizacion_can_macho': int(np.average(datos_esterilizacion_can_macho)),
        'promedio_esterlizacion_can_hembra': int(np.average(datos_esterilizacion_can_hembra)),
        'promedio_esterlizacion_fel_macho': int(np.average(datos_esterilizacion_fel_macho)),
        'promedio_esterlizacion_fel_hembra': int(np.average(datos_esterilizacion_fel_hembra)),
        #retiros y entrega
        'promedio_entrega': int(np.average(datos_entrega)),
        'promedio_retiro': int(np.average(datos_retiro)),
        #datos y etiquetas
        'lista_labels': json.dumps([label_cursos, label_year, label_curso_anios, label_libretas_anios,\
                                    label_analisis, label_categoria_analisis, label_categoria_patente,\
                                    label_categoria_esterilizacion, label_animales_anios]),
        'lista_datos': json.dumps([{'Inscripciones':datos_inscripciones},{'Cursos':datos_cursos_anuales},\
                                    {'Sin calificar':datos_sc,'Aprobados':datos_aprobados,'Desaprobados':datos_desaprobados},\
                                    {'Blancas':datos_blanca,'Amarillas':datos_amarilla,'Celestes':datos_celeste},\
                                    {'Analisis':datos_analisis},\
                                    {'Porker':datos_porker,'Lechon':datos_lechon,'Adulto':datos_adulto},\
                                    {'Can. Machos':datos_can_macho,'Can. Hembras':datos_can_hembra,\
                                    'Fel. Machos':datos_fel_macho,'Fel. Hembras':datos_fel_hembra},\
                                    {'Can. Machos':datos_esterilizacion_can_macho,'Can. Hembras':datos_esterilizacion_can_hembra,\
                                    'Fel. Machos':datos_esterilizacion_fel_macho,'Fel. Hembras':datos_esterilizacion_fel_hembra},\
                                    {'Entregados':datos_entrega,'Retirados':datos_retiro}])
    }



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

    for x in xrange(50):
        analisis = factories.AnalisisFactory()

    for x in xrange(50):
        mascotas = factories.MascotaFactory()

    for x in xrange(50):
        patentes = factories.PatenteFactory()

    for x in xrange(50):
        esterilizacion = factories.EsterilizacionFactory()

    for x in xrange(50):
        retiro_entrega = factories.RetiroEntregaAnimalFactory()
    '''


    return render(request, "estadistica/opciones_estadisticas.html", context)
