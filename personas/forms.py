# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import re
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class PersonaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())
    regex = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")

    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'dni', 'nacionalidad', 'obra_social', 'telefono', 'email',
                  'rubro']


class DomicilioForm(forms.ModelForm):

    class Meta:
        model = Domicilio
        fields = ['barrio', 'calle', 'nro', 'dpto', 'piso', 'localidad']

'''
persona juridica

  def clean_cuil(self):
        cuil = self.cleaned_data['cuil']
        if cuil:
            if PersonaFisica.objects.filter(cuil=cuil).exists():
                raise forms.ValidationError('Ya existe una persona con este CUIL')

            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuil):
                raise forms.ValidationError('CUIL inválido, por favor siga este formato XX-YYYYYYYY-Z')
        return cuil
'''