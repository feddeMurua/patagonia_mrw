# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import datetime
import string
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

    def clean_fecha_inicio(self):
        fecha = self.cleaned_data['fecha_inicio']
        if fecha:
            if fecha < datetime.date.today():
                raise forms.ValidationError('La fecha no puede ser menor que la actual')
        return fecha

    def clean_lugar(self):
        lugar = self.cleaned_data['lugar']
        if not CursoForm.regex.match(lugar):
                raise forms.ValidationError('El lugar no puede contener caracteres especiales')
        return lugar


class LibretaForm(forms.ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput())

    class Meta:
        model = LibretaSanitaria
        fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso', 'observaciones', 'fecha_examen_clinico',
                    'profesional_examen_clinico', 'lugar_examen_clinico', 'foto']


class InscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso', 'observaciones']

    def __init__(self, id_curso=None, *args, **kwargs):
        super(InscripcionForm, self).__init__(*args, **kwargs)
        curso = Curso.objects.get(pk=id_curso)
        self.fields['curso'].initial = curso
        self.fields['curso'].widget = forms.HiddenInput()
