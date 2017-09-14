# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect
from easy_pdf.views import PDFTemplateView
from .forms import *
from .filters import *
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView)


'''
CURSOS
'''


@login_required(login_url='login')
def lista_curso(request):
    lista_cursos = Curso.objects.all()
    filtro_cursos = CursoListFilter(request.GET, queryset=lista_cursos)
    fecha_hoy = datetime.date.today()
    return render(request, 'curso/curso_list.html', {'fecha_hoy': fecha_hoy, 'filter': filtro_cursos})


class AltaCurso(LoginRequiredMixin, CreateView):
    model = Curso
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    form_class = CursoForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def baja_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    curso.delete()
    return HttpResponse('ok')


class ModificacionCurso(LoginRequiredMixin, UpdateView):
    model = Curso
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    form_class = CursoForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def cierre_de_curso(request, id_curso):
    if request.method == 'POST':
        curso = Curso.objects.get(pk=id_curso)
        curso.finalizado = True
        curso.save()
        return redirect('cursos:lista_cursos')
    else:
        lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
        filtro_inscripciones = InscripcionListFilter(request.GET, queryset=lista_inscripciones)
        apto_cierre = True
        for inscripcion in lista_inscripciones:
            if not inscripcion.modificado:
                apto_cierre = False
                break
        return render(request, "curso/curso_cierre.html", {'id_curso': id_curso, 'filter': filtro_inscripciones,
                                                           'apto_cierre': apto_cierre})


'''
LIBRETRAS SANITARIAS
'''


@login_required(login_url='login')
def lista_libreta(request):
    lista_libretas = LibretaSanitaria.objects.all()
    filtro_libretas = LibretaListFilter(request.GET, queryset=lista_libretas)
    return render(request, 'libreta/libreta_list.html', {'filter': filtro_libretas})


class DetalleLibreta(LoginRequiredMixin, DetailView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaLibreta(LoginRequiredMixin, CreateView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_form.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    form_class = LibretaForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def baja_libreta(request, pk):
    libreta = LibretaSanitaria.objects.get(pk=pk)
    libreta.delete()
    return HttpResponse('ok')


class ModificacionLibreta(LoginRequiredMixin, UpdateView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_form.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    fields = ['observaciones', 'fecha_examen_clinico', 'profesional_examen_clinico', 'lugar_examen_clinico',
              'foto']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
INSCRIPCIONES
'''


@login_required(login_url='login')
def lista_inscripciones_curso(request, id_curso):
    lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
    filtro_inscripciones = InscripcionListFilter(request.GET, queryset=lista_inscripciones)
    curso = Curso.objects.get(pk=id_curso)
    cupo_restante = curso.cupo - len(lista_inscripciones)
    fecha_hoy = datetime.date.today()
    return render(request, "curso/curso_inscripciones.html", {'id_curso': id_curso, 'fecha_hoy': fecha_hoy,
                                                              'curso': curso, 'cupo_restante': cupo_restante,
                                                              'filter': filtro_inscripciones})


@login_required(login_url='login')
def alta_inscripcion(request, id_curso):
    if request.method == 'POST':
        form = InscripcionForm(request.POST, id_curso=id_curso)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.curso = Curso.objects.get(pk=id_curso)
            inscripcion.save()
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', args=id_curso))
    else:
        form = InscripcionForm
    url_return = 'cursos:inscripciones_curso'
    return render(request, "inscripcion/inscripcion_form.html", {'id_curso': id_curso, 'form': form,
                                                                     'url_return': url_return})


@login_required(login_url='login')
def baja_inscripcion(request, pk):
    inscripcion = Inscripcion.objects.get(pk=pk)
    inscripcion.delete()
    return HttpResponse('ok')


@login_required(login_url='login')
def modificacion_inscripcion(request, pk, id_curso):
    inscripcion = Inscripcion.objects.get(pk=pk)
    if request.method == 'POST':
        observaciones_form = ObservacionesForm(request.POST)
        if observaciones_form.is_valid():
            observaciones = observaciones_form.cleaned_data['observaciones']
            inscripcion.observaciones = observaciones
            inscripcion.save()
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', kwargs={'id_curso': id_curso}))
    else:
        form = ObservacionesForm(initial={'observaciones': inscripcion.observaciones})
        url_return = 'cursos:inscripciones_curso'
        return render(request, 'inscripcion/inscripcion_form.html', {'form': form, 'id_curso': id_curso,
                                                                     'url_return': url_return})


@login_required(login_url='login')
def cierre_inscripcion(request, pk, id_curso):
    if request.method == 'POST':
        inscripcion = Inscripcion.objects.get(pk=pk)
        inscripcion_form = CierreInscripcionForm(request.POST, instance=inscripcion)
        if inscripcion_form.is_valid():
            inscripcion_form.save()
            inscripcion.modificado = True
            inscripcion.save()
            return HttpResponseRedirect(reverse('cursos:cierre_curso', kwargs={'id_curso': id_curso}))
    else:
        form = CierreInscripcionForm
        url_return = 'cursos:cierre_curso'
        return render(request, 'inscripcion/inscripcion_form.html', {'form': form, 'id_curso': id_curso,
                                                                     'url_return': url_return})


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
