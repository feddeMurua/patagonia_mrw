# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django import forms
from .models import *


class DatePickerForm(forms.Form):
    fecha = forms.DateField()


class MovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = MoviemientoDiario
        exclude = ['fecha']
        fields = '__all__'
        labels = {
            'nro_ingreso': _("N° de ingresos varios")
        }


class DetalleMovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = DetalleMovimiento
        exclude = ['movimiento', 'titular', 'descripcion', 'servicio']
        fields = '__all__'
        labels = {
            'forma_pago': _("Forma de pago")
        }
