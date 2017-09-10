# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import datetime
import re
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class CursoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput())
    horario = forms.TimeField(widget=TimeInput())
    regex = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")

    class Meta:
        model = Curso
        fields = ['fecha_inicio', 'cupo', 'lugar', 'horario']


class LibretaForm(forms.ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput())

    class Meta:
        model = LibretaSanitaria
        fields = ['persona', 'curso', 'observaciones', 'fecha_examen_clinico', 'profesional_examen_clinico',
                  'lugar_examen_clinico', 'foto']


class InscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['persona', 'observaciones']


class CierreInscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['nota_curso', 'porcentaje_asistencia']


class ObservacionesForm(forms.Form):
    observaciones = forms.CharField(widget=forms.Textarea)
