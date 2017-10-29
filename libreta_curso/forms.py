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

regex_alfabetico = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")
regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class CursoForm(forms.ModelForm):

    class Meta:
        model = Curso
        fields = '__all__'
        exclude = ['finalizado']
        labels = {
            'fecha_inicio': _("Fecha y hora")
        }

    def clean_lugar(self):
        lugar = self.cleaned_data['lugar']
        if not regex_alfanumerico.match(lugar):
            raise forms.ValidationError('El nombre del lugar solo puede contener letras/numeros y/o espacios')
        return lugar

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio.time() < datetime.time(8, 0) or fecha_inicio.time() > datetime.time(22, 0):
            raise forms.ValidationError('Debe seleccionar un horario entre las 08:00 y las 22:00 hs.')
        return fecha_inicio


class InscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['persona', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 13, 'cols': 20})
        }

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


class ModificacionInscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }


class CierreInscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['nota_curso', 'porcentaje_asistencia']
        labels = {
            'nota_curso': _("Calificacion"),
            'porcentaje_asistencia': _("Porcentaje de asistencia")
        }


class LibretaForm(forms.ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput(), label="Fecha de examen clínico")

    class Meta:
        model = LibretaSanitaria
        exclude = ['fecha', 'curso', 'fecha_vencimiento']
        fields = '__all__'
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }
        labels = {
            'profesional_examen_clinico': _("Médico clínico"),
            'lugar_examen_clinico': _("Lugar de realizacion del examen"),
            'tipo_libreta': _("Tipo de libreta"),
            'meses_validez': _("Meses de validez")
        }

    def clean_profesional_examen_clinico(self):
        profesional_examen_clinico = self.cleaned_data['profesional_examen_clinico']
        if not regex_alfabetico.match(profesional_examen_clinico):
            raise forms.ValidationError('El nombre del médico clínico solo puede contener letras y/o espacios')
        return profesional_examen_clinico

    def clean_lugar_examen_clinico(self):
        lugar_examen_clinico = self.cleaned_data['lugar_examen_clinico']
        if not regex_alfanumerico.match(lugar_examen_clinico):
            raise forms.ValidationError('El nombre del lugar del examen clínico solo puede contener letras/numeros'
                                        'y/o espacios')
        return lugar_examen_clinico


class ModificacionLibretaForm(forms.ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput(), label="Fecha de examen clínico")

    class Meta:
        model = LibretaSanitaria
        exclude = ['persona', 'curso', 'fecha', 'fecha_vencimiento']
        fields = '__all__'
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }
        labels = {
            'profesional_examen_clinico': _("Médico clínico"),
            'lugar_examen_clinico': _("Lugar de realizacion del examen")
        }

    def clean_profesional_examen_clinico(self):
        profesional_examen_clinico = self.cleaned_data['profesional_examen_clinico']
        if not regex_alfabetico.match(profesional_examen_clinico):
            raise forms.ValidationError('El nombre del médico clínico solo puede contener letras y/o espacios')
        return profesional_examen_clinico

    def clean_lugar_examen_clinico(self):
        lugar_examen_clinico = self.cleaned_data['lugar_examen_clinico']
        if not regex_alfanumerico.match(lugar_examen_clinico):
            raise forms.ValidationError('El nombre del lugar del examen clínico solo puede contener letras/numeros'
                                        'y/o espacios')
        return lugar_examen_clinico
