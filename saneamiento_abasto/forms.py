# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})

class AbastecedorForm(forms.ModelForm):

    class Meta:
        model = Abastecedor
        fields = ['persona', 'empresa_y_o_transporte', 'rubro']


class ReinspeccionForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())
    turno = forms.TimeField(widget=TimeInput())
    class Meta:
        model = Reinspeccion
        fields = ['fecha', 'primer_inspector', 'segundo_inspector',
        'segundo_inspector', 'turno','precintado','num_certificado','abastecedor']
