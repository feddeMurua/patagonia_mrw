# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *
from django.utils.translation import ugettext as _
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin

DATEINPUT = partial(forms.DateInput, {'class': 'datepicker'})


class AbastecedorForm(forms.ModelForm):
    class Meta:
        model = Abastecedor
        exclude = ['cc']


class ListaAbastecedoresForm(forms.Form):
    abastecedor = forms.ModelChoiceField(queryset=Abastecedor.objects.all())


class ReinspeccionForm(forms.ModelForm):
    fecha = forms.DateField(widget=DATEINPUT(), label="Fecha de realizacion")
    inspectores = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = Reinspeccion
        exclude = ['total_kg']
        labels = {
            'certificado': _("N° de certificado")
        }


class ModificacionReinspeccionForm(forms.ModelForm):
    class Meta:
        model = Reinspeccion
        exclude = ['fecha', 'abastecedor', 'total_kg']


class AltaProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre']


class ReinspeccionProductoForm(forms.ModelForm):
    class Meta:
        model = ReinspeccionProducto
        fields = ['producto', 'kilo_producto']
        widgets = {
            'producto': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('reinspecciones:alta_producto'),
            )
        }
        labels = {
            'kilo_producto': _("Kg de producto")
        }


class ReinspeccionPreciosForm(forms.ModelForm):
    class Meta:
        model = ReinspeccionPrecios
        fields = '__all__'
        labels = {
            'precio_min': _("Monto mínimo"),
            'precio_kg': _("Precio por Kg")
        }


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['rubro_vehiculo']
        labels = {
            'tipo_vehiculo': _("Tipo de vehiculo"),
            'tipo_tpp': _("Tipo de transporte"),
            'disposicion_resolucion': _("Resolucion"),
            'nro': _('N°')
        }


class ModificarTSAForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['titular', 'tipo_vehiculo', 'rubro_vehiculo']
        labels = {
            'disposicion_resolucion': _("Disposicion")
        }


class ModificarTPPForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['titular', 'tipo_vehiculo', 'categoria', 'rubro_vehiculo']
        labels = {
            'disposicion_resolucion': _("Resolucion")
        }


class DesinfeccionForm(forms.ModelForm):
    class Meta:
        model = Desinfeccion
        fields = ['justificativo']


class ControlDePlagaForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DATEINPUT(), label="Fecha de próxima visita")
    funcionario_actuante = forms.ModelChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha_hoy', 'pagado']
        labels = {
            'tipo_plaga': _("Tipo de plaga")
        }

    def clean_fecha_prox_visita(self):
        fecha_prox_visita = self.cleaned_data['fecha_prox_visita']
        if fecha_prox_visita < timezone.now().date() + relativedelta(days=1):
            raise forms.ValidationError('La fecha seleccionada debe ser al menos 1 dia despues del control que se está'
                                        ' registrando')
        return fecha_prox_visita


class ModificacionControlDePlagaForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DATEINPUT(), label="Fecha de próxima visita")

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha_hoy', 'responsable', 'funcionario_actuante', 'pagado']
        labels = {
            'tipo_plaga': _("Tipo de plaga")
        }

    def clean_fecha_prox_visita(self):
        fecha_prox_visita = self.cleaned_data['fecha_prox_visita']
        if fecha_prox_visita < timezone.now().date() + relativedelta(days=1):
            raise forms.ValidationError('La fecha seleccionada debe ser al menos 1 dia despues del control que se está'
                                        ' registrando')
        return fecha_prox_visita


class PagoDiferidoForm(forms.ModelForm):
    class Meta:
        model = PagoDiferido        
        fields = ['fecha_pago']
