# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import *
from .choices import *


class MovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = MoviemientoDiario
        exclude = ('fecha',)
        fields = '__all__'


class DetalleMovimientoDiarioForm(forms.ModelForm):

    tipo_pago = forms.ChoiceField(choices=TipoPago, label="Tipo de Pago", initial='', widget=forms.Select())

    class Meta:
        model = DetalleMovimiento
        exclude = ('movimiento','titular','descripcion',)
        fields = '__all__'
