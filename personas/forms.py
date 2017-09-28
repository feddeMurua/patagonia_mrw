# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class ListaPersonasGenericasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaGenerica.objects.all())


class AltaPersonaFisicaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = PersonaFisica
        exclude = ['documentacion_retirada']
        fields = '__all__'


class AltaPersonaJuridicaForm(forms.ModelForm):

    class Meta:
        model = PersonaJuridica
        fields = '__all__'


class ModificacionPersonaFisicaForm(forms.ModelForm):

    class Meta:
        model = PersonaFisica
        fields = ['telefono', 'email', 'obra_social', 'rubro', 'documentacion_retirada']


class ListaPersonasFisicasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaFisica.objects.all(), required=True)


class DomicilioForm(forms.ModelForm):

    class Meta:
        model = Domicilio
        fields = '__all__'


class DomicilioRuralForm(forms.ModelForm):

    class Meta:
        model = DomicilioRural
        fields = '__all__'


class LocalidadForm(forms.ModelForm):

    class Meta:
        model = Localidad
        fields = '__all__'
