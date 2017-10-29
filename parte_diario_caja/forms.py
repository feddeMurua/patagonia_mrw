# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django import forms
from django.core.exceptions import ObjectDoesNotExist
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

    def clean_nro_ingreso(self):
        nro_ingreso = self.cleaned_data['nro_ingreso']
        try:
            movimiento = MovimientoDiario.objects.get(nro_ingreso=nro_ingreso)
            print (self.cleaned_data['titular'])
            if movimiento.titular != self.cleaned_data['titular']:
                raise forms.ValidationError(
                    'El N° de Ingresos Varios ingresado ya existe, a nombre de ' + str(movimiento.titular))
        except ObjectDoesNotExist:
            pass
        return nro_ingreso


class DetalleMovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = DetalleMovimiento
        exclude = ['movimiento', 'descripcion']
        fields = '__all__'
        labels = {
            'forma_pago': _("Forma de pago"),
            'nro_cheque': _("N° de cheque")
        }

    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo')
        super(DetalleMovimientoDiarioForm, self).__init__(*args, **kwargs)

        self.fields['servicio'] = forms.ModelChoiceField(queryset=Servicio.objects.filter(tipo__nombre=tipo))

