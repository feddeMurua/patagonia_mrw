# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
from .models import *
from django.utils.translation import ugettext as _
from django.utils import timezone
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.urlresolvers import reverse_lazy

DATEINPUT = partial(forms.DateInput, {'class': 'datepicker'})


class AbastecedorForm(forms.ModelForm):
    class Meta:
        model = Abastecedor
        exclude = ['cc']


class ListaAbastecedoresForm(forms.Form):
    abastecedor = forms.ModelChoiceField(queryset=Abastecedor.objects.all())


class ReinspeccionForm(forms.ModelForm):
    inspectores = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))
    total_kg = forms.IntegerField(required=True, label="Total de Kg inspeccionados")

    class Meta:
        model = Reinspeccion
        exclude = ['fecha', 'detalles']
        labels = {
            'certificado': _("N° de certificado")
        }
        widgets = {
            'origen': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_localidad'),
            )
        }


class ReinspeccionCCForm(forms.ModelForm):
    fecha = forms.DateField(widget=DATEINPUT(), label="Fecha de realizacion")
    inspectores = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = Reinspeccion
        fields = '__all__'
        labels = {
            'certificado': _("N° de certificado")
        }
        widgets = {
            'origen': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_localidad'),
            )
        }


class ModificarReinspeccionForm(forms.ModelForm):
    fecha = forms.DateField(widget=DATEINPUT(), label="Fecha de realizacion")
    inspectores = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = Reinspeccion
        fields = ['fecha', 'turno', 'precintado', 'inspectores', 'origen']


class AltaProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if Producto.objects.filter(nombre__iexact=nombre).last():
            self.add_error('nombre', forms.ValidationError('El producto ingresado ya se encuentra registrado en el'
                                                           'sistema'))


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
            'anio': _("Año"),
            'tipo_vehiculo': _("Tipo de vehiculo"),
            'tipo_tpp': _("Tipo de transporte"),
            'disposicion_resolucion': _("Resolucion N°"),
            'nro': _('N°')
        }
        widgets = {
            'modelo': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('vehiculo:alta_modelo'),
            )
        }


class MarcaVehiculoForm(forms.ModelForm):
    class Meta:
        model = MarcaVehiculo
        fields = '__all__'


class ModeloVehiculoForm(forms.ModelForm):
    class Meta:
        model = ModeloVehiculo
        fields = '__all__'
        widgets = {
            'marca': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('vehiculo:alta_marca'),
            )
        }


class ModificarTSAForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['titular', 'tipo_tpp', 'tipo_vehiculo', 'rubro_vehiculo']
        labels = {
            'disposicion_resolucion': _("Disposicion")
        }
        widgets = {
            'modelo': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('vehiculo:alta_modelo'),
            )
        }


class ModificarTPPForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['titular', 'tipo_vehiculo', 'categoria', 'rubro_vehiculo']
        labels = {
            'disposicion_resolucion': _("Resolucion"),
            'tipo_tpp': _('Tipo de transporte'),
            'nro': _('N°')
        }
        widgets = {
            'modelo': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('vehiculo:alta_modelo'),
            )
        }


class DesinfeccionForm(forms.ModelForm):
    class Meta:
        model = Desinfeccion
        fields = ['justificativo']


class ControlDePlagaForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DATEINPUT(), label="Fecha de próxima visita", required=True)
    funcionario_actuante = forms.ModelChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Inspector'))

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha', 'pagado']
        labels = {
            'tipo_plaga': _("Tipo de plaga")
        }
        widgets = {
            'recomendaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }

    def clean_fecha_prox_visita(self):
        fecha_prox_visita = self.cleaned_data['fecha_prox_visita']
        if fecha_prox_visita <= timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser al menos 1 dia despues del control que se está'
                                        ' registrando')
        return fecha_prox_visita


class ModificacionControlDePlagaForm(forms.ModelForm):

    class Meta:
        model = ControlDePlaga
        exclude = ['fecha', 'responsable', 'funcionario_actuante', 'pagado']
        labels = {
            'tipo_plaga': _("Tipo de plaga")
        }
        widgets = {
            'recomendaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }


class VisitaControlForm(forms.ModelForm):
    fecha_prox_visita = forms.DateField(widget=DATEINPUT(), label="Fecha de próxima visita", required=False)

    class Meta:
        model = VisitaControl
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }

    def clean_fecha_prox_visita(self):
        fecha_prox_visita = self.cleaned_data['fecha_prox_visita']
        if fecha_prox_visita and fecha_prox_visita <= timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser al menos 1 dia despues de la visita que se está'
                                        ' registrando')
        return fecha_prox_visita


class ModificacionVisitaControlForm(forms.ModelForm):
    fecha = forms.DateField(widget=DATEINPUT())

    class Meta:
        model = VisitaControl
        fields = ['fecha']

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha <= timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser al menos 1 dia despues de la fecha actual')
        return fecha


class PagoDiferidoForm(forms.ModelForm):
    class Meta:
        model = PagoDiferido        
        fields = ['fecha_pago']
