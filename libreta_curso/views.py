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


'''
CURSOS
'''


@login_required(login_url='login')
def lista_curso(request):
    return render(request, 'curso/curso_list.html', {'fecha_hoy': now, 'listado': Curso.objects.all()})


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

    def get_context_data(self, pk):     #pk del curso por paŕametro
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

    def get_context_data(self, pk):     #pk del curso por paŕametro
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
    return render(request, "curso/curso_inscripciones.html", {'fecha_hoy': now, 'cupo_restante': cupo_restante,
                                                              'listado': lista_inscripciones, 'curso': curso})


@login_required(login_url='login')
def alta_inscripcion(request, id_curso):
    if request.method == 'POST':
        form = InscripcionForm(request.POST, id_curso=id_curso)
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST,
                                                                   tipo='Curso de Manipulacion de Alimentos')
        if form.is_valid() & mov_diario_form.is_valid() & detalle_mov_diario_form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.curso = Curso.objects.get(pk=id_curso)
            inscripcion.save()
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " N° " + str(inscripcion.id)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip)
            detalle_mov_diario.save()
            log_crear(request.user.id, inscripcion, 'Inscripcion a Curso')
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', args=id_curso))
    else:
        form = InscripcionForm
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Curso de Manipulacion de Alimentos')
    url_return = 'cursos:inscripciones_curso'
    return render(request, "inscripcion/inscripcion_form.html", {'id_curso': id_curso, 'url_return': url_return,
                                                                 'form': form, 'mov_diario_form': mov_diario_form,
                                                                 'detalle_mov_diario_form': detalle_mov_diario_form})


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
            inscripcion=inscripcion,
            title="Detalle de Inscripcion"
        )


'''
LIBRETRAS SANITARIAS
'''


def get_cursos(pk_persona):
    inscripciones = Inscripcion.objects.filter(persona__pk=pk_persona)
    cursos = []
    for inscripcion in inscripciones:
        if inscripcion.nota_curso == 'Aprobado':
            cursos.append(inscripcion.curso)
    return cursos


@login_required(login_url='login')
def lista_libreta(request):
    return render(request, 'libreta/libreta_list.html', {'listado': LibretaSanitaria.objects.all()})


@login_required(login_url='login')
def alta_libreta(request):
    if request.method == 'POST':
        form = LibretaForm(request.POST)
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Libreta Sanitaria')
        if form.is_valid() & mov_diario_form.is_valid() & detalle_mov_diario_form.is_valid():
            libreta = form.save(commit=False)
            cursos = get_cursos(libreta.persona.pk)
            if cursos:
                libreta.curso = cursos[-1]
            libreta.save()
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " N° " + str(libreta.id)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip)
            detalle_mov_diario.save()
            log_crear(request.user.id, libreta, 'Libreta Sanitaria')
            return redirect('libretas:lista_libretas')
    else:
        form = LibretaForm
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Libreta Sanitaria')
    return render(request, 'libreta/libreta_form.html', {'form': form, 'mov_diario_form': mov_diario_form,
                                                         'detalle_mov_diario_form': detalle_mov_diario_form})


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
            log_modificar(request.user.id, form.save(), 'Libreta Sanitaria')
            return redirect('libretas:lista_libretas')
    else:
        form = ModificacionLibretaForm(instance=libreta)
    return render(request, 'libreta/libreta_form.html', {'form': form, 'modificacion': True})
