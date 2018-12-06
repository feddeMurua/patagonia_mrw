# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import re
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import *
from django.utils.translation import ugettext as _

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

regex_alfabetico = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")
regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class CursoForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = Curso
        exclude = ['finalizado']

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super(CursoForm, self).__init__(*args, **kwargs)

    def clean_lugar(self):
        lugar = self.cleaned_data['lugar']
        if not regex_alfanumerico.match(lugar):
            raise forms.ValidationError('El nombre del lugar solo puede contener letras/numeros y/o espacios')
        return lugar

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date() + relativedelta(days=7) and not self.usuario.is_staff:
            raise forms.ValidationError('Debe haber al menos una semana de diferencia entre la fecha de inicio '
                                        'seleccionada y la fecha actual')
        return fecha


class ModificacionCursoForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = Curso
        exclude = ['finalizado']

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super(ModificacionCursoForm, self).__init__(*args, **kwargs)

    def clean_lugar(self):
        lugar = self.cleaned_data['lugar']
        if not regex_alfanumerico.match(lugar):
            raise forms.ValidationError('El nombre del lugar solo puede contener letras/numeros y/o espacios')
        return lugar

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date() + relativedelta(days=1) and not self.usuario.is_staff:
            raise forms.ValidationError('La fecha seleccionada debe ser posterior al dia de hoy')
        return fecha

    def clean_cupo(self):
        cupo = self.cleaned_data['cupo']
        inscriptos = len(Inscripcion.objects.filter(curso=self.instance))
        if cupo < inscriptos:
            raise forms.ValidationError('El cupo no puede ser menor a la cantidad de alumnos previamiente inscriptos')
        return cupo


class InscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['persona', 'observaciones', 'rubro']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
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
        fields = ['calificacion', 'porcentaje_asistencia']
        labels = {
            'porcentaje_asistencia': _("Porcentaje de asistencia")
        }


class RegistroInscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        exclude = ['curso', 'modificado']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }


class LibretaForm(forms.ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput())

    class Meta:
        model = LibretaSanitaria
        exclude = ['fecha', 'curso', 'fecha_vencimiento', 'foto']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
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

    def clean_fecha_examen_clinico(self):
        fecha_examen_clinico = self.cleaned_data['fecha_examen_clinico']
        if fecha_examen_clinico > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return fecha_examen_clinico


class ModificacionLibretaForm(forms.ModelForm):

    class Meta:
        model = LibretaSanitaria
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }


class RenovacionLibretaForm(forms.ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput())

    class Meta:
        model = LibretaSanitaria
        exclude = ['persona', 'curso', 'fecha', 'fecha_vencimiento', 'tipo_libreta', 'foto']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
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

    def clean_fecha_examen_clinico(self):
        fecha_examen_clinico = self.cleaned_data['fecha_examen_clinico']
        if fecha_examen_clinico > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return fecha_examen_clinico
