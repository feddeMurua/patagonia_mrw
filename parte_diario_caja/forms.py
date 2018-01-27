# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django import forms
from .models import *
from django.utils import timezone
import re
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.urlresolvers import reverse_lazy

regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class DatePickerForm(forms.Form):
    fecha = forms.DateField()

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return fecha


class MovimientoDiarioForm(forms.ModelForm):

    class Meta:
        model = MovimientoDiario
        exclude = ['fecha']
        fields = '__all__'
        labels = {
            'nro_ingreso': _("N° de ingresos varios"),
            'forma_pago': _("Forma de pago"),
            'nro_cheque': _("N° de cheque")
        }


class DetalleMovimientoDiarioForm(forms.ModelForm):
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
        exclude = ['fecha', 'debito_credito_cant', 'debito_credito_sub', 'cheques_cant', 'cheques_sub',
                   'mov_efectivo_sis', 'sub_efectivo_sis', 'mov_tarjeta_sis', 'mov_tarjeta_sis', 'sub_tarjeta_sis',
                   'mov_cheque_sis', 'sub_cheque_sis', 'mov_total_sistema', 'imp_total_sistema']
        fields = '__all__'
        labels = {
            'nro_planilla': _("N° de planilla"),
            'billetes_quinientos': _("Billetes de quinientos ($500,00)"),
            'billetes_doscientos': _("Billetes de Doscientos ($200,00)"),
            'billetes_cien': _("Billetes de cien ($100,00)"),
            'billetes_cincuenta': _("Billetes de cincuenta ($50,00)"),
            'billetes_veinte': _("Billetes de veinte ($20,00)"),
            'billetes_diez': _("Billetes de diez ($10,00)"),
            'billetes_cinco': _("Billetes de cinco ($5,00)"),
            'billetes_dos': _("Billetes de dos ($2,00)"),
            'monedas_dos': _("Monedas de dos ($2,00)"),
            'monedas_uno': _("Monedas de uno ($1,00)"),
            'monedas_cincuenta': _("Monedas de cincuenta ctvs ($0,50)"),
            'monedas_veinticinco': _("Monedas de veinticinco ctvs. ($0,25)"),
            'total_manual': _("Total de recuento manual")
        }


class ArqueoOtrosForm(forms.ModelForm):

    class Meta:
        model = ArqueoDiario
        fields = ['debito_credito_cant', 'debito_credito_sub', 'cheques_cant', 'cheques_sub']


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = '__all__'
