# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext as _
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
        labels = {
            'categoria_porcino': _("Categoria del porcino")
        }


AltaPorcinoFormSet = formset_factory(PorcinoForm, min_num=1, validate_min=True, extra=0)

ModificacionPorcinoFormSet = forms.modelformset_factory(Porcino, fields=('precinto', 'categoria_porcino'), extra=0)


class SolicitudForm(forms.ModelForm):
    categoria_criadero = forms.ChoiceField(choices=Categoria_Criadero, initial='', widget=forms.Select(),
                                           label="Categoria del criadero")

    class Meta:
        model = SolicitudCriaderoCerdos
        fields = ['interesado', 'categoria_criadero']


class AplazoSolicitudForm(forms.ModelForm):

    class Meta:
        model = AplazoSolicitud
        fields = ['motivo_aplazo']
        widgets = {
            'motivo_aplazo': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }
        labels = {
            'motivo_aplazo': _("Motivo del aplazo")
        }


class DisposicionForm(forms.ModelForm):
    fecha_disposicion = forms.DateField(widget=DateInput(), label="Fecha de emision de disposicion")

    class Meta:
        model = DisposicionCriaderoCerdos
        fields = ['nro_disposicion', 'fecha_disposicion']
        labels = {
            'nro_disposicion': _("N° de disposicion")
        }


class TurnoForm(forms.Form):
    turno = forms.DateTimeField(required=True)


class MascotaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput(), label="Fecha de nacimiento")

    class Meta:
        model = Mascota
        exclude = ['baja']
        fields = '__all__'
        labels = {
            'categoria_mascota': _("Categoria de la mascota"),

        }


class PatenteForm(forms.ModelForm):

    class Meta:
        model = Patente
        fields = ['persona', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }


class ControlAntirrabicoForm(forms.ModelForm):
    fecha_suceso = forms.DateField(widget=DateInput(), label="Fecha del suceso")

    class Meta:
        model = ControlAntirrabico
        fields = '__all__'
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }


class VisitaForm(forms.ModelForm):

    class Meta:
        model = Visita
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        }


class RetiroEntregaForm(forms.ModelForm):

    class Meta:
        model = RetiroEntregaAnimal
        fields = ['tramite', 'observaciones', 'patentado']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        }


class ListaPatentesForm(forms.Form):
    patente = forms.ModelChoiceField(queryset=Patente.objects.all(), required=True)
