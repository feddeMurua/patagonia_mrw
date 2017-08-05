# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from easy_pdf.views import PDFTemplateView
from .forms import *
from .filters import *
from .models import *
from .choices import *
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)


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


class BajaCurso(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'curso/curso_confirm_delete.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionCurso(LoginRequiredMixin, UpdateView):
    model = Curso
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    form_class = CursoForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def cierre_de_curso(request, id_curso):
    lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
    filtro_inscripciones = InscripcionListFilter(request.GET, queryset=lista_inscripciones)
    apto_cierre = True
    for inscripcion in lista_inscripciones:
        if not inscripcion.modificado:
            apto_cierre = False
    if apto_cierre:
        curso = Curso.objects.get(id=id_curso)
        curso.finalizado = True
        curso.save()
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


class BajaLibreta(LoginRequiredMixin, DeleteView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_confirm_delete.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionLibreta(LoginRequiredMixin, UpdateView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_form.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    fields = ['observaciones', 'fecha_examen_clinico', 'profesional_examen_clinico', 'lugar_examen_clinico',
              'foto']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
PERSONAS
'''


@login_required(login_url='login')
def lista_persona(request):
    lista_personas = PersonaFisica.objects.all()
    filtro_personas = InscripcionListFilter(request.GET, queryset=lista_personas)
    return render(request, 'persona/persona_list.html', {'filter': filtro_personas})


@login_required(login_url='login')
def lista_detalles_persona(request, id_persona):
    persona = PersonaFisica.objects.get(id=id_persona)
    lista_cursos_inscripciones = Inscripcion.objects.filter(persona__id=id_persona)
    return render(request, "persona/persona_detail.html", {'persona': persona,
                                                           'inscripciones': lista_cursos_inscripciones})


class AltaPersona(LoginRequiredMixin, CreateView):
    model = PersonaFisica
    template_name = 'persona/persona_form.html'
    success_url = reverse_lazy('personas:lista_personas')
    form_class = PersonaForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaPersona(LoginRequiredMixin, DeleteView):
    model = PersonaFisica
    template_name = 'persona/persona_confirm_delete.html'
    success_url = reverse_lazy('personas:lista_personas')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionPersona(LoginRequiredMixin, UpdateView):
    model = PersonaFisica
    template_name = 'persona/persona_form.html'
    success_url = reverse_lazy('personas:lista_personas')
    fields = ['obra_social', 'domicilio', 'telefono', 'email', 'rubro', 'documentacion_retirada']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

'''
INSCRIPCIONES
'''


class DetalleInscripcion(LoginRequiredMixin, DetailView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


def lista_inscripciones_curso(request, id_curso):
    lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
    filtro_inscripciones = InscripcionListFilter(request.GET, queryset=lista_inscripciones)
    return render(request, "curso/curso_inscripciones.html", {'id_curso': id_curso, 'filter': filtro_inscripciones})


class AltaInscripcion(CreateView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_form.html'
    form_class = InscripcionForm

    def get_success_url(self):
        if 'id_curso' in self.kwargs:
            id_curso = self.kwargs['id_curso']
        return reverse('cursos:inscripciones_curso', kwargs={'id_curso': id_curso})

    def get_form_kwargs(self):
        kwargs = super(AltaInscripcion, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs


class BajaInscripcion(LoginRequiredMixin, DeleteView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_confirm_delete.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_success_url(self):
        if 'id_curso' in self.kwargs:
            id_curso = self.kwargs['id_curso']
        return reverse('cursos:inscripciones_curso', kwargs={'id_curso': id_curso})


class ModificacionInscripcion(LoginRequiredMixin, UpdateView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_form.html'
    fields = ['observaciones']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_success_url(self):
        if 'id_curso' in self.kwargs:
            id_curso = self.kwargs['id_curso']
        return reverse('cursos:cierre_curso', kwargs={'id_curso': id_curso})


class CierreCursoInscripcion(ModificacionInscripcion):
    nota_curso = forms.ChoiceField(choices=Calificaciones, label="Calificacion", initial='', widget=forms.Select())

    fields = ['nota_curso', 'porcentaje_asistencia']

    def get_success_url(self):
        if 'id_curso' in self.kwargs:
            id_curso = self.kwargs['id_curso']
            inscripcion = Inscripcion.objects.get(pk=self.kwargs['pk'])
            inscripcion.modificado = True
            inscripcion.save()
        return reverse('cursos:cierre_curso', kwargs={'id_curso': id_curso})


class pdfInscripcion(PDFTemplateView):
    template_name = 'inscripcion/inscripcion_pdf.html'

    def get_context_data(self, pk, id_curso):
        inscripcion = Inscripcion.objects.get(pk=pk)
        return super(pdfInscripcion, self).get_context_data(
            pagesize="A4",
            inscripcion=inscripcion,
            title="Detalle de Inscripcion"
        )

