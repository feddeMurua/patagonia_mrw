# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms.formsets import formset_factory
from functools import partial
from .models import *
from .choices import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class AltaAnalisisForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())
    medico_veterinario = forms.ModelMultipleChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Veterinario'))

    class Meta:
        model = Analisis
        fields = '__all__'


class ModificacionAnalisisForm(forms.ModelForm):
    categoria = forms.ChoiceField(choices=Categorias, label="Categoria", initial='', widget=forms.Select())
    resultado = forms.ChoiceField(choices=Resultados, label="Resultado", initial='', widget=forms.Select())

    class Meta:
        model = Analisis
        fields = ['procedencia', 'resultado', 'categoria']


class PorcinoForm(forms.ModelForm):

    class Meta:
        model = Porcino
        fields = ['precinto', 'categoria_porcino']


AltaPorcinoFormSet = formset_factory(PorcinoForm, min_num=1, validate_min=True, extra=0)

ModificacionPorcinoFormSet = forms.modelformset_factory(Porcino, fields=('precinto', 'categoria_porcino'), extra=0)


class SolicitudForm(forms.ModelForm):
    categoria_criadero = forms.ChoiceField(choices=Categoria_Criadero, label="Categoria", initial='',
                                           widget=forms.Select())

    class Meta:
        model = SolicitudCriaderoCerdos
        fields = ['interesado', 'categoria_criadero']


class AplazoSolicitudForm(forms.ModelForm):

    class Meta:
        model = AplazoSolicitud
        fields = ['motivo_aplazo']


class DisposicionForm(forms.ModelForm):
    fecha_disposicion = forms.DateField(widget=DateInput())

    class Meta:
        model = DisposicionCriaderoCerdos
        fields = ['nro_disposicion', 'fecha_disposicion']


class TurnoForm(forms.Form):
    turno = forms.DateTimeField(required=True)


class MascotaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = Mascota
        exclude = ['baja']
        fields = '__all__'


class PatenteForm(forms.ModelForm):

    class Meta:
        model = Patente
        fields = ['persona', 'observaciones', 'nro_ingreso_varios', 'tipo_pago']


class ControlAntirrabicoForm(forms.ModelForm):

    class Meta:
        model = ControlAntirrabico
        fields = ['mordido', 'responsable', 'observaciones']


class VisitaForm(forms.ModelForm):

    class Meta:
        model = Visita
        fields = ['observaciones']


class RetiroEntregaForm(forms.ModelForm):

    class Meta:
        model = RetiroEntregaAnimal
        fields = ['tramite', 'observaciones', 'patentado']


class ListaPatentesForm(forms.Form):
    patente = forms.ModelChoiceField(queryset=Patente.objects.all(), required=True)
