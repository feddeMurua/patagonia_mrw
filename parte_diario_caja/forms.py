# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import partial
from django import forms
from .models import *


class DatePickerForm(forms.Form):
    fecha = forms.DateField()


class MovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = MoviemientoDiario
        exclude = ['fecha']
        fields = '__all__'


class DetalleMovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = DetalleMovimiento
        exclude = ['movimiento', 'titular', 'descripcion', 'servicio']
        fields = '__all__'
