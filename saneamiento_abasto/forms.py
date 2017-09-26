# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *
from django.utils.translation import ugettext as _


DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class AbastecedorForm(forms.ModelForm):    

    class Meta:
        model = Abastecedor
        fields = '__all__'


class ReinspeccionForm(forms.ModelForm):
    inspectores = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = Reinspeccion
        fields = '__all__'


class ReinspeccionProductoForm(forms.ModelForm):

    class Meta:
        model = ReinspeccionProducto
        fields = ['producto', 'kilo_producto']

    def __init__(self, *args, **kwargs):
        self.id_curso = kwargs.pop('reinspeccion_pk', None)
        super(ReinspeccionProductoForm, self).__init__(*args, **kwargs)

    def clean_producto(self):
        producto = self.cleaned_data['producto']
        reinspecciones = ReinspeccionProductoForm.objects.filter(producto__pk=producto.pk)
        if reinspecciones:
            reinspeccion_pk = int(self.reinspeccion_pk)
            for reinspeccion in reinspecciones:
                if reinspeccion.pk == reinspeccion_pk:
                    raise forms.ValidationError(_('Este producto ya se encuentra cargado en la reinspeccion'),
                                                code='invalid')
        return producto


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = '__all__'


class DesinfeccionForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = Desinfeccion
        fields = ['fecha', 'quincena', 'vehiculo']


class ControlDePlagaForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DateInput(), required=False)

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha_hoy']
        fields = '__all__'
