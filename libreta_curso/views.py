# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from .models import (
    PersonaFisica,
    LibretaSanitaria,
    Curso,
    Inscripcion,
    ExamenClinico   )

'''
CURSOS
'''

class ListaCurso(ListView):
    model = Curso


class DetalleCurso(DetailView):
    model = Curso


class AltaCurso(CreateView):
    model = Curso
    success_url = reverse_lazy('lista_cursos')
    fields = ['fecha_inicio','cupo','lugar','horario','precio']


class BajaCurso(DeleteView):
    model = Curso
    success_url = reverse_lazy('lista_cursos')


class ModificacionCurso(UpdateView):
    model = Curso
    success_url = reverse_lazy('lista_cursos')
    fields = ['fecha_inicio','cupo','lugar','horario','precio']
