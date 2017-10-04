# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django import forms
from .models import *


class DatePickerForm(forms.Form):
    fecha = forms.DateField()


class MovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = MovimientoDiario
        exclude = ['fecha']
        fields = '__all__'
        labels = {
            'nro_ingreso': _("N° de ingresos varios")
        }


class DetalleMovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = DetalleMovimiento
        exclude = ['movimiento', 'titular', 'descripcion']
        fields = '__all__'
        labels = {
            'forma_pago': _("Forma de pago")
        }

    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo')
        super(DetalleMovimientoDiarioForm, self).__init__(*args, **kwargs)

        self.fields['servicio'] = forms.ModelChoiceField(queryset=Servicio.objects.filter(tipo__nombre=tipo))
