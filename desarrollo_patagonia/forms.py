# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from django.utils import timezone

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class RangoFechaForm(forms.Form):
    fecha_desde = forms.DateField(widget=DateInput(), label='Fecha desde', required=True)
    fecha_hasta = forms.DateField(widget=DateInput(), label='Fecha hasta', required=True)

    def clean(self):
        cleaned_data = super(RangoFechaForm, self).clean()
        fecha_desde = cleaned_data.get('fecha_desde')
        fecha_hasta = cleaned_data.get('fecha_hasta')
        msg = "La fecha seleccionada debe ser menor a la fecha actual"
        if fecha_desde > timezone.now().date():
            self.add_error('fecha_desde', msg)
        elif fecha_hasta > timezone.now().date():
            self.add_error('fecha_hasta', msg)
        if fecha_desde > fecha_hasta:
            raise forms.ValidationError('La fecha de inicio de rango no puede ser mayor a la fecha de fin de rango')


class RangoAnioForm(forms.Form):
    anio_choice = [tuple([x, x]) for x in range(timezone.now().year, 1999, -1)]
    anio_desde = forms.ChoiceField(choices=anio_choice, label="Año desde")
    anio_hasta = forms.ChoiceField(choices=anio_choice, label="Año hasta")

    def clean(self):
        cleaned_data = super(RangoAnioForm, self).clean()
        anio_desde = cleaned_data.get('anio_desde')
        anio_hasta = cleaned_data.get('anio_hasta')
        if anio_desde > anio_hasta:
            raise forms.ValidationError('El año de inicio de rango no puede ser mayor al año de fin de rango')
