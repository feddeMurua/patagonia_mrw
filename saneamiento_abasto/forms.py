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
        labels = {
            'num_certificado': _("N° de certificado")
        }


class ModificacionReinspeccionForm(forms.ModelForm):

    class Meta:
        model = Reinspeccion
        exclude = ['abastecedor']
        fields = '__all__'


class ReinspeccionProductoForm(forms.ModelForm):

    class Meta:
        model = ReinspeccionProducto
        fields = ['producto', 'kilo_producto']
        labels = {
            'kilo_producto': _("Kg de producto")
        }

    def __init__(self, *args, **kwargs):
        self.reinspeccion_pk = kwargs.pop('reinspeccion_pk', None)
        super(ReinspeccionProductoForm, self).__init__(*args, **kwargs)

    def clean_producto(self):
        producto = self.cleaned_data['producto']
        reinspecciones = ReinspeccionProducto.objects.filter(producto__pk=producto.pk)
        if reinspecciones:
            reinspeccion_pk = int(self.reinspeccion_pk)
            for reinspeccion in reinspecciones:
                if reinspeccion.pk == reinspeccion_pk:
                    raise forms.ValidationError(_('Este producto ya se encuentra cargado en la reinspeccion'),
                                                code='invalid')
        return producto


class ModificacionReinspeccionProductoForm(forms.ModelForm):

    class Meta:
        model = ReinspeccionProducto
        fields = ['kilo_producto']
        labels = {
            'kilo_producto': _("Kg de producto")
        }


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        exclude = ['rubro_vehiculo']
        fields = '__all__'
        labels = {
            'tipo_vehiculo': _("Tipo de vehiculo"),
            'disposicion_resolucion': _("Resolucion")
        }


class ModificarTSAForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        exclude = ['titular', 'tipo_vehiculo', 'rubro_vehiculo']
        fields = '__all__'
        labels = {
            'disposicion_resolucion': _("Disposicion")
        }


class ModificarTPPForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        exclude = ['titular', 'tipo_vehiculo', 'categoria', 'rubro_vehiculo']
        fields = '__all__'
        labels = {
            'disposicion_resolucion': _("Resolucion")
        }


class DesinfeccionForm(forms.ModelForm):

    class Meta:
        model = Desinfeccion
        fields = ['justificativo']


class ControlDePlagaForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DateInput(), label="Fecha de próxima visita")
    funcionario_actuante = forms.ModelChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha_hoy']
        fields = '__all__'
        labels = {
            'tipo_plaga': _("Tipo de plaga")
        }


class ModificacionControlDePlagaForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DateInput(), label="Fecha de próxima visita")

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha_hoy', 'responsable', 'funcionario_actuante']
        fields = '__all__'
        labels = {
            'tipo_plaga': _("Tipo de plaga")
        }
