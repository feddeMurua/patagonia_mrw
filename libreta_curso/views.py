# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.shortcuts import render
from .forms import *
from .filters import (
    CursoListFilter,
    LibretaListFilter,
    PersonaListFilter,
    ExamenListFilter,
    InscripcionListFilter)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from .models import (
    LibretaSanitaria,
    Curso,
    PersonaFisica,
    ExamenClinico,
    Inscripcion)


'''
CURSOS
'''


def ListaCurso(request):
    lista_cursos = Curso.objects.all()
    filtro_cursos = CursoListFilter(request.GET, queryset=lista_cursos)
    return render(request, 'curso/curso_list.html', {'filter': filtro_cursos})


class DetalleCurso(DetailView):
    model = Curso
    template_name = 'curso/curso_detail.html'


class AltaCurso(CreateView):
    model = Curso
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    form_class = CursoForm


class BajaCurso(DeleteView):
    model = Curso
    template_name = 'curso/curso_confirm_delete.html'
    success_url = reverse_lazy('cursos:lista_cursos')


class ModificacionCurso(UpdateView):
    model = Curso
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    form_class = CursoForm


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


def ListaLibreta(request):
    lista_libretas = LibretaSanitaria.objects.all()
    filtro_libretas = LibretaListFilter(request.GET, queryset=lista_libretas)
    return render(request, 'libreta/libreta_list.html', {'filter': filtro_libretas})


class DetalleLibreta(DetailView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_detail.html'


class AltaLibreta(CreateView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_form.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso',
                'observaciones', 'examen_clinico', 'foto']


class BajaLibreta(DeleteView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_confirm_delete.html'
    success_url = reverse_lazy('libretas:lista_libretas')


class ModificacionLibreta(UpdateView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_form.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso',
                'observaciones', 'examen_clinico', 'foto']


'''
PERSONAS
'''


def ListaPersona(request):
    lista_personas = PersonaFisica.objects.all()
    filtro_personas = PersonaListFilter(request.GET, queryset=lista_personas)
    return render(request, 'persona/persona_list.html', {'filter': filtro_personas})


class DetallePersona(DetailView):
    model = PersonaFisica
    template_name = 'persona/persona_detail.html'


class AltaPersona(CreateView):
    model = PersonaFisica
    template_name = 'persona/persona_form.html'
    success_url = reverse_lazy('personas:lista_personas')
    form_class = PersonaForm


class BajaPersona(DeleteView):
    model = PersonaFisica
    template_name = 'persona/persona_confirm_delete.html'
    success_url = reverse_lazy('personas:lista_personas')


class ModificacionPersona(UpdateView):
    model = PersonaFisica
    template_name = 'persona/persona_form.html'
    success_url = reverse_lazy('personas:lista_personas')
    fields = ['obra_social', 'domicilio', 'telefono', 'email', 'rubro']


'''
EXAMENES CLINICOS
'''


def ListaExamen(request):
    lista_examenes = ExamenClinico.objects.all()
    filtro_examenes = ExamenListFilter(request.GET, queryset=lista_examenes)
    return render(request, 'examen/examen_list.html', {'filter': filtro_examenes})


class DetalleExamen(DetailView):
    model = ExamenClinico
    template_name = 'examen/examen_detail.html'


class AltaExamen(CreateView):
    model = ExamenClinico
    template_name = 'examen/examen_form.html'
    success_url = reverse_lazy('examenes:lista_examenes')
    form_class = ExamenForm


class BajaExamen(DeleteView):
    model = ExamenClinico
    template_name = 'examen/examen_confirm_delete.html'
    success_url = reverse_lazy('examenes:lista_examenes')


'''
INSCRIPCIONES
'''


def ListaInscripcion(request):
    lista_inscripciones = Inscripcion.objects.all()
    filtro_inscripciones = InscripcionListFilter(request.GET, queryset=lista_inscripciones)
    return render(request, 'inscripcion/inscripcion_list.html', {'filter': filtro_inscripciones})


class DetalleInscripcion(DetailView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_detail.html'


class AltaInscripcion(CreateView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_form.html'
    success_url = reverse_lazy('inscripciones:lista_inscripciones')
    fields = ['nro_ingresos_varios', 'arancel','persona','curso', 'observaciones']


class BajaInscripcion(DeleteView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_confirm_delete.html'
    success_url = reverse_lazy('inscripciones:lista_inscripciones')


class ModificacionInscripcion(UpdateView):
    model = Inscripcion
    template_name = 'inscripcion/inscripcion_form.html'
    success_url = reverse_lazy('inscripciones:lista_inscripciones')
    fields = ['nro_ingresos_varios', 'arancel','persona', 'curso', 'observaciones']
