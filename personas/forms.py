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
        fields = ['barrio', 'calle', 'calle_entre1', 'calle_entre2', 'nro', 'dpto', 'piso', 'localidad']


class DomicilioRuralForm(forms.ModelForm):

    class Meta:
        model = DomicilioRural
        fields = ['chacra', 'parcela', 'sector', 'circunscripcion', 'ruta']


class LocalidadForm(forms.ModelForm):

    class Meta:
        model = Localidad
        fields = ['nombre', 'cp', 'provincia']
