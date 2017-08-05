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


class PersonaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())
    regex = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")

    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'cuil', 'fecha_nacimiento', 'dni', 'nacionalidad', 'obra_social',
                  'domicilio', 'telefono', 'email', 'rubro']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not PersonaForm.regex.match(nombre):
            raise forms.ValidationError('El nombre de la persona solo puede contener letras y espacios')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not PersonaForm.regex.match(apellido):
            raise forms.ValidationError('El apellido de la persona solo puede contener letras y espacios')
        return apellido

    def clean_cuil(self):
        cuil = self.cleaned_data['cuil']
        if cuil:
            if PersonaFisica.objects.filter(cuil=cuil).exists():
                raise forms.ValidationError('Ya existe una persona con este CUIL')

            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuil):
                raise forms.ValidationError('CUIL inválido, por favor siga este formato XX-YYYYYYYY-Z')
        return cuil

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not re.match(r"^[0-9]{7,}$", dni):
            raise forms.ValidationError('El dni de la persona debe contener al menos 7 digitos')
        return dni

    def clean_nacionalidad(self):
        nacionalidad = self.cleaned_data['nacionalidad']
        if not PersonaForm.regex.match(nacionalidad):
            raise forms.ValidationError('La nacionalidad de la persona solo puede contener letras y espacios')
        return nacionalidad

    def clean_obra_social(self):
        obra_social = self.cleaned_data['obra_social']
        if not PersonaForm.regex.match(obra_social):
                raise forms.ValidationError('La obra social de la persona no puede contener caracteres especiales')
        return obra_social

    def clean_domicilio(self):
        domicilio = self.cleaned_data['domicilio']
        regex = re.compile(r"^[a-zñA-ZÑ\d]+((\s[a-zñA-ZÑ\d]+)+)?$")
        if not regex.match(domicilio):
                raise forms.ValidationError('El domicilio de la persona no puede contener caracteres especiales')
        return domicilio

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not re.match(r"^[0-9]{2,}-[0-9]{6,}$", telefono):
            raise forms.ValidationError('Teléfono inválido, por favor siga este formato PREFIJO-NUMERO (yyyy-nnnnnnnn)')
        return telefono

    def clean_rubro(self):
        rubro = self.cleaned_data['rubro']
        if not PersonaForm.regex.match(rubro):
            raise forms.ValidationError('El rubro de la persona solo puede contener letras y espacios')
        return rubro


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
        fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso',
                    'observaciones', 'fecha_examen_clinico',
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
