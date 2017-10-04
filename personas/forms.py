# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django import forms
from functools import partial
from django.utils.translation import ugettext as _
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class ListaUsuariosForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())


class ListaPersonasGenericasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaGenerica.objects.all(), required=True)


class ListaPersonasFisicasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaFisica.objects.all(), required=True)


class ListaPersonasJuridicasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaJuridica.objects.all(), required=True)


class AltaPersonaFisicaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput(), label="Fecha de nacimiento")

    class Meta:
        model = PersonaFisica
        exclude = ['documentacion_retirada', 'domicilio']
        fields = '__all__'


class AltaPersonaJuridicaForm(forms.ModelForm):

    class Meta:
        model = PersonaJuridica
        exclude = ['domicilio']
        fields = '__all__'


class ModificacionPersonaFisicaForm(forms.ModelForm):

    class Meta:
        model = PersonaFisica
        fields = ['telefono', 'email', 'obra_social', 'rubro', 'documentacion_retirada']


class DomicilioForm(forms.ModelForm):

    class Meta:
        model = Domicilio
        fields = '__all__'
        labels = {
            'calle_entre1': _("Entre"),
            'calle_entre2': _("Entre"),
            'nro': _("N°"),
            'dpto': _("Departamento")
        }


class DomicilioRuralForm(forms.ModelForm):

    class Meta:
        model = DomicilioRural
        fields = '__all__'


class LocalidadForm(forms.ModelForm):

    class Meta:
        model = Localidad
        fields = '__all__'
        labels = {
            'cp': _("Código postal")
        }
