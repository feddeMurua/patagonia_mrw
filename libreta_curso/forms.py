# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import re
import datetime
from .models import *
from django.utils.translation import ugettext as _

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class CursoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput())
    horario = forms.TimeField(widget=TimeInput())

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

    def __init__(self, *args, **kwargs):
        self.id_curso = kwargs.pop('id_curso', None)
        super(InscripcionForm, self).__init__(*args, **kwargs)

    def clean_persona(self):
        persona = self.cleaned_data['persona']
        inscripciones = Inscripcion.objects.filter(persona__pk=persona.pk)
        if inscripciones:
            id_curso = int(self.id_curso)
            for inscripcion in inscripciones:
                if inscripcion.curso.pk == id_curso:
                    raise forms.ValidationError(_('Ya existe una inscripcion a este curso a nombre de la persona '
                                                  'seleccionada'), code='invalid')
        return persona


class CierreInscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['nota_curso', 'porcentaje_asistencia']


class ObservacionesForm(forms.Form):
    observaciones = forms.CharField(widget=forms.Textarea)
