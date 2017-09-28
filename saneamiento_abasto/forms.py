# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *
from .choices import *
from django.utils.translation import ugettext as _


DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class ReinspeccionForm(forms.ModelForm):
    inspectores = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = Reinspeccion
        fields = '__all__'
        labels = {
            'num_certificado': _("N° de certificado")
        }


class ReinspeccionProductoForm(forms.ModelForm):

    class Meta:
        model = ReinspeccionProducto
        fields = ['producto', 'kilo_producto']
        labels = {
            'kilo_producto': _("Kg de producto")
        }

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
        exclude = ['rubro_vehiculo']
        fields = '__all__'
        labels = {
            'tipo_vehiculo': _("Tipo de vehiculo"),
            'disposicion_resolucion': _("Resolucion")
        }


class ModificarVehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        exclude = ['dominio', 'titular', 'tipo_vehiculo', 'rubro_vehiculo']
        fields = '__all__'


class DesinfeccionForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = Desinfeccion
        fields = ['fecha', 'quincena', 'vehiculo']


class ControlDePlagaForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DateInput(), label="Fecha de próxima visita")

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha_hoy']
        fields = '__all__'
        labels = {
            'tipo_plaga': _("Tipo de plaga")
        }
