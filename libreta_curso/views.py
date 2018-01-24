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
from parte_diario_caja import models as pd_m
from desarrollo_patagonia import forms as dp_f
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from dateutil.relativedelta import *
from django.utils import timezone
import json
import numpy as np
import collections
from desarrollo_patagonia import factories


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
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', kwargs={'id_curso': id_curso}))
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
        if form.is_valid() & detalle_mov_form.is_valid():
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
            detalle_mov.completar(pd_m.Servicio.objects.get(nombre="Alta de libreta sanitaria"), libreta)
            log_crear(request.user.id, libreta, 'Libreta Sanitaria')
            return redirect('libretas:lista_libretas')
    else:
        form = LibretaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
    return render(request, 'libreta/libreta_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form})


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


@login_required(login_url='login')
def renovacion_libreta(request, pk):
    libreta = LibretaSanitaria.objects.get(pk=pk)
    if request.method == 'POST':
        form = RenovacionLibretaForm(request.POST, instance=libreta)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        if form.is_valid() & detalle_mov_form.is_valid():
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
            detalle_mov.completar(pd_m.Servicio.objects.get(nombre="Renovacion de libreta sanitaria"), libreta)
            log_crear(request.user.id, libreta, 'Renovacion de Libreta Sanitaria')
            return redirect('libretas:lista_libretas')
    else:
        form = RenovacionLibretaForm(instance=libreta)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        return render(request, 'libreta/libreta_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form})


'''
ESTADÍSTICAS
'''


@login_required(login_url='login')
def estadisticas_lc(request):
    rango_form = dp_f.RangoFechaForm
    anio = timezone.now().year
    years = range(anio, anio - 5, -1)
    cursos = Curso.objects.filter(fecha__year__gt=years[-1])
    if request.method == 'POST':
        rango_form = dp_f.RangoFechaForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']
            anio_desde = fecha_desde.year
            anio_hasta = fecha_hasta.year
            years = range(anio_hasta, anio_desde - 1, -1)
            cursos = Curso.objects.filter(fecha__gte=fecha_desde, fecha__lte=fecha_hasta)

    # diccionario de datos
    aprobados_curso = {}
    desaprobados_curso = {}
    s_c_curso = {}

    cursos_anuales = {}

    libretas_blancas = {}
    libretas_amarillas = {}
    libretas_celestes = {}

    for year in years:

        # acumuladores
        s_c = 0
        aprobados = 0
        desaprobados = 0

        cursos_anio = Inscripcion.objects.filter(curso__fecha__year=year).values_list("calificacion")

        for nota in cursos_anio:
            if nota[0] == "Sin Calificar":
                s_c += 1
            elif nota[0] == "Aprobado":
                aprobados += 1
            else:
                desaprobados += 1

        s_c_curso[str(year)] = s_c
        aprobados_curso[str(year)] = aprobados
        desaprobados_curso[str(year)] = desaprobados


        cursos_anuales[str(year)] = Curso.objects.filter(fecha__year=year).count()


        # acumuladores
        blancas = 0
        amarillas = 0
        celestes = 0

        libretras_anio = LibretaSanitaria.objects.filter(fecha__year=year).values_list("tipo_libreta")

        for color in libretras_anio:
            if color[0] == "Blanca":
                blancas += 1
            elif color[0] == "Amarilla":
                amarillas += 1
            else:
                celestes += 1

        libretas_blancas[str(year)] = blancas
        libretas_amarillas[str(year)] = amarillas
        libretas_celestes[str(year)] = celestes

    # CALIFICACIONES

    ord_s_c_curso = collections.OrderedDict(sorted(s_c_curso.items()))
    ord_aprobados = collections.OrderedDict(sorted(aprobados_curso.items()))
    ord_desaprobados = collections.OrderedDict(sorted(desaprobados_curso.items()))

    label_curso_anios = ord_s_c_curso.keys()  # indistinto para los datos (tienen la misma clave)
    datos_sc = ord_s_c_curso.values()
    datos_aprobados = ord_aprobados.values()
    datos_desaprobados = ord_desaprobados.values()

    # CURSOS POR AÑO

    ord_cursos_anuales = collections.OrderedDict(sorted(cursos_anuales.items()))

    label_year = ord_cursos_anuales.keys()
    datos_cursos_anuales = ord_cursos_anuales.values()

    # INSCRIPCIONES A CURSO

    inscripciones = {}  # inscripciones por curso

    for curso in cursos:
        inscripciones[str(curso.fecha)] = Inscripcion.objects.filter(curso__fecha=curso.fecha).count()

    ord_inscripciones = collections.OrderedDict(sorted(inscripciones.items()))

    label_cursos = ord_inscripciones.keys()
    if cursos:
        datos_inscripciones = ord_inscripciones.values()
    else:
        datos_inscripciones = 0

    # LIBRETAS POR TIPO

    ord_libretas_blancas = collections.OrderedDict(sorted(libretas_blancas.items()))
    ord_libretas_amarillas = collections.OrderedDict(sorted(libretas_amarillas.items()))
    ord_libretas_celestes = collections.OrderedDict(sorted(libretas_celestes.items()))

    label_libretas_anios = ord_libretas_blancas.keys() # indistinto para los datos (tienen la misma clave)
    datos_blanca = ord_libretas_blancas.values()
    datos_amarilla = ord_libretas_amarillas.values()
    datos_celeste = ord_libretas_celestes.values()

    '''
    CONTEXTO
    '''

    context = {
        'rango_form': rango_form,
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
        # datos y etiquetas
        'lista_labels': json.dumps([label_cursos, label_year, label_curso_anios, label_libretas_anios]),
        'lista_datos': json.dumps([{'Inscripciones': datos_inscripciones}, {'Cursos': datos_cursos_anuales},
                                   {'Sin calificar': datos_sc, 'Aprobados': datos_aprobados, 'Desaprobados': datos_desaprobados},
                                   {'Blancas': datos_blanca, 'Amarillas': datos_amarilla, 'Celestes': datos_celeste}])
    }

    return render(request, "estadistica/estadisticas_lc.html", context)
