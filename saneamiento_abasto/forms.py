# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *
from personas import models as m


DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class AbastecedorForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = Abastecedor
        fields = ['nombre', 'domicilio', 'telefono', 'email', 'apellido', 'fecha_nacimiento', 'dni', 'nacionalidad',
                  'obra_social', 'empresa']


class RazonSocialForm(forms.Form):
    razon_social = forms.CharField(max_length=25, required=True)


class ReinspeccionForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())
    turno = forms.TimeField(widget=TimeInput())

    class Meta:
        model = Reinspeccion
        fields = '__all__'


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = '__all__'

    '''
    def clean(self):
        check = [self.cleaned_data['persona'], self.cleaned_data['abastecedor']]
        if any(check) and not all(check):
            cleaned_data = self.cleaned_data
            vehiculo = cleaned_data.get("vehiculo")
            if Transporte.objects.filter(vehiculo=vehiculo).exists():
                raise ValidationError('Atencion! ya existe este vehículo registrado, por favor seleccione otro')
            return self.cleaned_data
        raise ValidationError('Por favor, seleccione una opcion (Abastecedor o Persona Particular)')
    '''


class DesinfeccionForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = Desinfeccion
        fields = ['fecha', 'quincena', 'vehiculo']
