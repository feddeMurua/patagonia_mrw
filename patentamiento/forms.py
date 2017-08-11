# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class MascotaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())    

    class Meta:
        model = Mascota
        fields = ['nombre', 'pelaje', 'raza', 'fecha_nacimiento', 'sexo']


class PatenteForm(forms.ModelForm):    

    class Meta:
        model = Patente
        fields = ['nro_ingresos_varios','arancel', 'persona', 'mascota', 'observaciones']

        