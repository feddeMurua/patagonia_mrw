# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils import timezone


class RangoEventosForm(forms.Form):
    fecha_desde = forms.DateTimeField(label='Fecha desde', required=True)
    fecha_hasta = forms.DateTimeField(label='Fecha hasta', required=True)

    def clean_fecha_hasta(self):
        fecha_hasta = self.cleaned_data['fecha_hasta']
        if fecha_hasta.date() > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser menor a la fecha actual')
        return fecha_hasta

    def clean_fecha_desde(self):
        fecha_desde = self.cleaned_data['fecha_desde']
        if fecha_desde.date() > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser menor a la fecha actual')
        return fecha_desde
