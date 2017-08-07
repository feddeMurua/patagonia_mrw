# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
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
