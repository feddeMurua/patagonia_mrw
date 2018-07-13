# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django import forms
from .models import *
from django.utils import timezone
from functools import partial
import re

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class DatePickerForm(forms.Form):
    fecha = forms.DateField(widget=DateInput(), label="Fecha")

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return fecha


class MovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = MovimientoDiario
        exclude = ['fecha']


class DetalleMovimientoDiarioForm(forms.ModelForm):
    movimiento = forms.ModelChoiceField(queryset=MovimientoDiario.objects.filter(fecha=timezone.now().date()))

    class Meta:
        model = DetalleMovimiento
        fields = ['movimiento']


class ListaServicios(forms.Form):
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all())

    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo')
        super(ListaServicios, self).__init__(*args, **kwargs)

        self.fields['servicio'] = forms.ModelChoiceField(queryset=Servicio.objects.filter(tipo__nombre=tipo))


class ArqueoEfectivoForm(forms.ModelForm):

    class Meta:
        model = ArqueoDiario
        exclude = ['fecha', 'tarjeta_cant', 'tarjeta_sub', 'cheques_cant', 'cheques_sub',
                   'mov_efectivo_sis', 'sub_efectivo_sis', 'mov_tarjeta_sis', 'mov_tarjeta_sis', 'sub_tarjeta_sis',
                   'mov_cheque_sis', 'sub_cheque_sis', 'mov_total_sistema', 'imp_total_sistema']
        labels = {
            'nro_planilla': _("N° de planilla"),
            'mil': _("Billetes de $1000,00"),
            'quinientos': _("Billetes de $500,00"),
            'doscientos': _("Billetes de $200,00"),
            'cien': _("Billetes de $100,00"),
            'b_cincuenta': _("Billetes de $50,00"),
            'veinte': _("Billetes de $20,00"),
            'diez': _("Billetes de $10,00"),
            'cinco': _("Billetes de $5,00"),
            'm_dos': _("Monedas de $2,00"),
            'uno': _("Monedas de $1,00"),
            'm_cincuenta': _("Monedas de $0,50"),
            'veinticinco': _("Monedas de $0,25"),
            'total_manual': _("Total de recuento manual")
        }


class ArqueoOtrosForm(forms.ModelForm):

    class Meta:
        model = ArqueoDiario
        fields = ['tarjeta_cant', 'tarjeta_sub', 'cheques_cant', 'cheques_sub']


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = '__all__'
