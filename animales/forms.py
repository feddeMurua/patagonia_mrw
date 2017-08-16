# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms.formsets import formset_factory
from functools import partial
from .models import *
from .choices import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class AnalisisForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())
    categoria = forms.ChoiceField(choices=Categorias, label="Categoria", initial='', widget=forms.Select())
    resultado = forms.ChoiceField(choices=Resultados, label="Resultado", initial='', widget=forms.Select())
    
    class Meta:
        model = Analisis
        fields = ['fecha', 'nro_ingreso', 'interesado', 'procedencia', 'medico_veterinario', 'resultado', 'categoria']


class PorcinoForm(forms.ModelForm):
    class Meta:
        model = Porcino
        fields = ['precinto', 'categoria_porcino']

PorcinoFormSet = formset_factory(PorcinoForm, min_num=1)


class HabilitacionForm(forms.ModelForm):
    fecha_disposicion = forms.DateField(widget=DateInput())   
    
    class Meta:
        model = HabilitacionCriaderoCerdos
        fields = ['fecha_disposicion', 'nro_disposicion', 'interesado']


class EsterilizacionForm(forms.ModelForm):    
    turno = forms.TimeField(widget=TimeInput())
    
    class Meta:
        model = Esterilizacion
        fields = ['turno', 'interesado']


class MascotaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = Mascota
        fields = ['nombre', 'pelaje', 'raza', 'fecha_nacimiento', 'sexo']


class PatenteForm(forms.ModelForm):

    class Meta:
        model = Patente
        fields = ['persona', 'mascota', 'observaciones']
