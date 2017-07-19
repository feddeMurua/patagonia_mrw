# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.shortcuts import render
from .forms import *
from .filters import *
from .models import *
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)



'''
CURSOS
'''


@login_required(login_url='login')
def ListaCurso(request):
    lista_cursos = Curso.objects.all()
    filtro_cursos = CursoListFilter(request.GET, queryset=lista_cursos)
    return render(request, 'curso/curso_list.html', {'filter': filtro_cursos})


class DetalleCurso(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = 'curso/curso_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


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

'''
@login_required(login_url='login')
def InscripcionesCurso(request, pk_curso):
    inscripciones_json = []
    inscripciones = Inscripcion.objects.filter(curso__pk=pk_curso)
    for inscripcion in inscripciones:
        inscripciones_json.append(inscripcion.to_json())
    return render(request, "curso/curso_inscripciones.html", {'inscripciones': inscripciones_json})
'''


@login_required(login_url='login')
def cierre_de_curso(request, pk_curso):
    pass

'''
pseudo codigo cierre de curso:

1) listar fecha con cursos menor < hoy (los que se cargaron en el dia no se pueden cerrar)
2) listar los alumnos pertenecientes al curso que se selecciono para cerrar
3) seleccionar un alumno inscripto, agregar nota y portecentaje de asistencia
4) repetir mietras haya alumnos en la lista
5) confirmar la operacion luego de repasar los datos ingresados
6) emitir certificado para todos los alumnos
7) fin

'''


'''
LIBRETRAS SANITARIAS
'''


@login_required(login_url='login')
def ListaLibreta(request):
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
    fields = ['nro_ingresos_varios', 'arancel', 'curso',
                'observaciones', 'fecha_examen_clinico',
                'profesional_examen_clinico', 'lugar_examen_clinico', 'foto']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

'''
PERSONAS
'''


@login_required(login_url='login')
def ListaPersona(request):
    lista_personas = PersonaFisica.objects.all()
    filtro_personas = PersonaListFilter(request.GET, queryset=lista_personas)
    return render(request, 'persona/persona_list.html', {'filter': filtro_personas})


class DetallePersona(LoginRequiredMixin, DetailView):
    model = PersonaFisica
    template_name = 'persona/persona_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


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
    fields = ['obra_social', 'domicilio', 'telefono', 'email', 'rubro']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

'''
INSCRIPCIONES
'''


@login_required(login_url='login')
def ListaInscripcion(request):
    lista_inscripciones = Inscripcion.objects.all()
    filtro_inscripciones = InscripcionListFilter(request.GET, queryset=lista_inscripciones)
    return render(request, 'inscripcion/inscripcion_list.html', {'filter': filtro_inscripciones})


class DetalleInscripcion(LoginRequiredMixin, DetailView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaInscripcion(LoginRequiredMixin, CreateView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_form.html'
    success_url = reverse_lazy('inscripciones:lista_inscripciones')
    fields = ['nro_ingresos_varios', 'arancel','persona','curso', 'observaciones']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaInscripcion(LoginRequiredMixin, DeleteView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_confirm_delete.html'
    success_url = reverse_lazy('inscripciones:lista_inscripciones')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionInscripcion(LoginRequiredMixin, UpdateView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_form.html'
    success_url = reverse_lazy('inscripciones:lista_inscripciones')
    fields = ['nro_ingresos_varios', 'arancel','persona', 'curso', 'observaciones']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
