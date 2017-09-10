# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import re
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class AltaPersonaFisicaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'dni', 'nacionalidad', 'telefono', 'email', 'obra_social',
                  'rubro']


class ModificacionPersonaFisicaForm(forms.ModelForm):

    class Meta:
        model = PersonaFisica
        fields = ['telefono', 'email', 'obra_social', 'rubro', 'documentacion_retirada']


class DomicilioForm(forms.ModelForm):

    class Meta:
        model = Domicilio
        fields = ['barrio', 'calle', 'nro', 'dpto', 'piso', 'localidad']


class DomicilioRuralForm(forms.ModelForm):

    class Meta:
        model = DomicilioRural
        fields = ['chacra', 'parcela', 'sector', 'circunscripcion', 'ruta']


class LocalidadForm(forms.ModelForm):

    class Meta:
        model = Localidad
        fields = ['nombre', 'cp', 'provincia']


'''
persona juridica

  def clean_cuil(self):
        cuil = self.cleaned_data['cuil']
        if cuil:
            if PersonaFisica.objects.filter(cuil=cuil).exists():
                raise forms.ValidationError('Ya existe una persona con este CUIL')

            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuil):
                raise forms.ValidationError('CUIL inválido, por favor siga este formato XX-YYYYYYYY-Z')
        return cuil
'''