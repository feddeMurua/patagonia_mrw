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
TIMEINPUT = partial(forms.TimeInput, {'class': 'timepicker'})


class AbastecedorForm(forms.ModelForm):
    class Meta:
        model = Abastecedor
        exclude = ['cc']
        fields = '__all__'


class ReinspeccionForm(forms.ModelForm):
    inspectores = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = Reinspeccion
        fields = '__all__'
        exclude = ['fecha', 'cc']
        labels = {
            'num_certificado': _("N° de certificado")
        }


class ModificacionReinspeccionForm(forms.ModelForm):
    class Meta:
        model = Reinspeccion
        exclude = ['fecha', 'abastecedor', 'cc']
        fields = '__all__'

    def clean_turno(self):
        turno = self.cleaned_data['turno']
        if turno.time() < datetime.time(8, 0) or turno.time() > datetime.time(22, 0):
            raise forms.ValidationError('Debe seleccionar un horario entre las 08:00 y las 22:00 hs.')
        elif turno.date() < timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser menor a la fecha actual')
        return turno


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
        fields = '__all__'
        labels = {
            'tipo_vehiculo': _("Tipo de vehiculo"),
            'tipo_tpp': _("Tipo de transporte"),
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
    fecha_prox_visita = forms.DateField(widget=DATEINPUT(), label="Fecha de próxima visita")
    funcionario_actuante = forms.ModelChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha_hoy', 'pagado']
        fields = '__all__'
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
        fields = '__all__'
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


class PagoCCForm(forms.ModelForm):
    class Meta:
        model = PagoCC
        fields = ['monto']
        labels = {
            'monto': _("Monto a cancelar")
        }
