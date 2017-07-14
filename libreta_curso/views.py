# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from .models import (
    LibretaSanitaria,
    Curso,
    PersonaFisica)

'''
CURSOS
'''


class ListaCurso(ListView):
    model = Curso
    template_name = 'curso/curso_list.html'


class DetalleCurso(DetailView):
    model = Curso
    template_name = 'curso/curso_detail.html'


class AltaCurso(CreateView):
    model = Curso
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    fields = ['fecha_inicio', 'cupo', 'lugar', 'horario']


class BajaCurso(DeleteView):
    model = Curso
    template_name = 'curso/curso_confirm_delete.html'
    success_url = reverse_lazy('cursos:lista_cursos')


class ModificacionCurso(UpdateView):
    model = Curso
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    fields = ['fecha_inicio', 'cupo', 'lugar', 'horario']


'''
LIBRETRAS SANITARIAS
'''


class ListaLibreta(ListView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_list.html'


class DetalleLibreta(DetailView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_detail.html'


class AltaLibreta(CreateView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_form.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso',
                'observaciones','examen_clinico','foto']


class BajaLibreta(DeleteView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_confirm_delete.html'
    success_url = reverse_lazy('libretas:lista_libretas')


class ModificacionLibreta(UpdateView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_form.html'
    success_url = reverse_lazy('libretas:lista_libretas')
    fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso',
                'observaciones','examen_clinico','foto']


'''
PERSONAS
'''


class ListaPersona(ListView):
    model = PersonaFisica
    template_name = 'persona/persona_list.html'


class DetallePersona(DetailView):
    model = PersonaFisica
    template_name = 'persona/persona_detail.html'


class AltaPersona(CreateView):
    model = PersonaFisica
    template_name = 'persona/persona_form.html'
    success_url = reverse_lazy('personas:lista_personas')
    fields = ['apellido', 'nombre', 'cuil', 'fecha_nacimiento', 'dni', 'nacionalidad', 'obra_social',
              'domicilio', 'telefono', 'email', 'rubro']


class BajaPersona(DeleteView):
    model = PersonaFisica
    template_name = 'persona/persona_confirm_delete.html'
    success_url = reverse_lazy('personas:lista_personas')


class ModificacionPersona(UpdateView):
    model = PersonaFisica
    template_name = 'persona/persona_form.html'
    success_url = reverse_lazy('personas:lista_personas')
    fields = ['obra_social', 'domicilio', 'telefono', 'email', 'rubro']