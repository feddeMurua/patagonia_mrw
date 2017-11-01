# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext as _
from functools import partial
from .models import *
from .choices import *
import re
import datetime

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})

regex_alfabetico = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")
regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class AltaAnalisisForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())
    medico_veterinario = forms.ModelChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Medico'))

    class Meta:
        model = Analisis
        fields = '__all__'


class ModificacionAnalisisForm(forms.ModelForm):

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

    def clean_turno(self):
        turno = self.cleaned_data['turno']
        if turno.time() < datetime.time(8, 0) or turno.time() > datetime.time(12, 0):
            raise forms.ValidationError('Debe seleccionar un horario entre las 08:00 y las 12:00 hs.')
        return turno


class MascotaForm(forms.ModelForm):
    nacimiento_fecha = forms.DateField(widget=DateInput(), label="Fecha de nacimiento", required=False)

    class Meta:
        model = Mascota
        exclude = ['baja']
        fields = '__all__'
        labels = {
            'categoria_mascota': _("Categoria de la mascota"),

        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not regex_alfabetico.match(nombre):
            raise forms.ValidationError('El nombre de la mascota, solo puede contener letras/numeros y/o espacios')
        return nombre

    def clean_pelaje(self):
        pelaje = self.cleaned_data['pelaje']
        if not regex_alfabetico.match(pelaje):
            raise forms.ValidationError('El pelaje de la mascota, solo puede contener letras/numeros y/o espacios')
        return pelaje

    def clean_raza(self):
        raza = self.cleaned_data['raza']
        if not regex_alfabetico.match(raza):
            raise forms.ValidationError('La raza de la mascota, solo puede contener letras/numeros y/o espacios')
        return raza


class PatenteForm(forms.ModelForm):

    class Meta:
        model = Patente
        fields = ['persona', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }


class ModificacionPatenteForm(forms.ModelForm):

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


class EsterilizacionPatenteForm(forms.Form):
    patente = forms.ModelChoiceField(queryset=Patente.objects.all(), required=True)
    turno = forms.DateTimeField(required=True)
