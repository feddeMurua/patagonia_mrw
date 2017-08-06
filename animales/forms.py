# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import datetime
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class AnalisisForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = Analisis
        fields = ['fecha', 'nro_ingreso', 'interesado', 'procedencia', 'medico_veterinario', 'resultado']
