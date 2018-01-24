# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from django.utils import timezone

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class RangoFechaForm(forms.Form):
    fecha_desde = forms.DateField(widget=DateInput(), label='Fecha desde', required=True)
    fecha_hasta = forms.DateField(widget=DateInput(), label='Fecha hasta', required=True)

    def clean_fecha_hasta(self):
        fecha_hasta = self.cleaned_data['fecha_hasta']
        if fecha_hasta > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser menor a la fecha actual')
        return fecha_hasta

    def clean_fecha_desde(self):
        fecha_desde = self.cleaned_data['fecha_desde']
        if fecha_desde > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser menor a la fecha actual')
        return fecha_desde
