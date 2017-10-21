# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django import forms
from functools import partial
import re
from django.utils.translation import ugettext as _
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

regex_alfabetico = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")
regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class ListaUsuariosForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())


class ListaPersonasGenericasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaGenerica.objects.all(), required=True)


class ListaPersonasFisicasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaFisica.objects.all(), required=True)


class ListaPersonasJuridicasForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=PersonaJuridica.objects.all(), required=True)


class PersonaGenericaForm(forms.ModelForm):

    class Meta:
        abstract = True

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not regex_alfabetico.match(nombre):
            raise forms.ValidationError('El nombre de la persona, solo puede contener letras y/o espacios')
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not re.match(r"^[0-9]{2,}-[0-9]{6,}$", telefono):
            raise forms.ValidationError('Teléfono inválido, por favor siga este formato PREFIJO-NUMERO (yyyy-nnnnnnnn)')
        return telefono


class AltaPersonaFisicaForm(PersonaGenericaForm):
    fecha_nacimiento = forms.DateField(widget=DateInput(), label="Fecha de nacimiento")

    class Meta:
        model = PersonaFisica
        exclude = ['documentacion_retirada', 'domicilio']
        fields = '__all__'

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not regex_alfabetico.match(apellido):
            raise forms.ValidationError('El apellido de la persona, solo puede contener letras y/o espacios')
        return apellido

    def clean_cuil(self):
        cuil = self.cleaned_data['cuil']
        if cuil:
            if PersonaFisica.objects.filter(cuil=cuil).exists():
                raise forms.ValidationError('Ya existe una persona con este CUIL')

            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuil):
                raise forms.ValidationError('CUIL inválido, por favor siga este formato XX-YYYYYYYY-Z')
        return cuil

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not re.match(r"^[0-9]{7,}$", dni):
            raise forms.ValidationError('El dni de la persona debe contener al menos 7 digitos y ser númerico')
        return dni

    def clean_obra_social(self):
        obra_social = self.cleaned_data['obra_social']
        if obra_social:
            if not regex_alfanumerico.match(obra_social):
                raise forms.ValidationError('La obra social de la persona, solo puede contener letras/numeros y/o espacios')
        return obra_social

    def clean_rubro(self):
        rubro = self.cleaned_data['rubro']
        if rubro:
            if not regex_alfabetico.match(rubro):
                raise forms.ValidationError('El rubro de la persona solo puede contener letras y espacios')
        return rubro


class ModificacionPersonaFisicaForm(forms.ModelForm):

    class Meta:
        model = PersonaFisica
        fields = ['telefono', 'email', 'obra_social', 'rubro', 'documentacion_retirada']

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not re.match(r"^[0-9]{2,}-[0-9]{6,}$", telefono):
            raise forms.ValidationError('Teléfono inválido, por favor siga este formato PREFIJO-NUMERO (yyyy-nnnnnnnn)')
        return telefono

    def clean_obra_social(self):
        obra_social = self.cleaned_data['obra_social']
        if obra_social:
            if not regex_alfanumerico.match(obra_social):
                raise forms.ValidationError('La obra social de la persona, solo puede contener letras/numeros y/o espacios')
        return obra_social

    def clean_rubro(self):
        rubro = self.cleaned_data['rubro']
        if rubro:
            if not regex_alfabetico.match(rubro):
                raise forms.ValidationError('El rubro de la persona solo puede contener letras y espacios')
        return rubro


class AltaPersonaJuridicaForm(forms.ModelForm):

    class Meta:
        model = PersonaJuridica
        exclude = ['domicilio']
        fields = '__all__'


class AltaPersonalPropioForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput(), label="Fecha de nacimiento")

    class Meta:
        model = PersonaFisica
        exclude = ['documentacion_retirada', 'domicilio']
        fields = '__all__'


class ModificacionPersonaJuridicaForm(forms.ModelForm):

    class Meta:
        model = PersonaJuridica
        exclude = ['nombre', 'cuit']
        fields = '__all__'


class ModificacionPersonalPropioForm(forms.ModelForm):

    class Meta:
        model = PersonalPropio
        fields = ['telefono', 'email', 'obra_social', 'rubro', 'documentacion_retirada', 'rol_actuante']


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

    def clean_barrio(self):
        barrio = self.cleaned_data['barrio']
        if barrio:
            if not regex_alfanumerico.match(barrio):
                raise forms.ValidationError('El nombre del barrio, solo puede contener letras/números y/o espacios')
        return barrio

    def clean_calle(self):
        calle = self.cleaned_data['calle']
        if not regex_alfanumerico.match(calle):
            raise forms.ValidationError('El nombre de la calle, solo puede contener letras/números y/o espacios')
        return calle

    def clean_calle_entre1(self):
        calle_entre1 = self.cleaned_data['calle_entre1']
        if calle_entre1:
            if not regex_alfanumerico.match(calle_entre1):
                raise forms.ValidationError('El nombre de la calle, solo puede contener letras/números y/o espacios')

        return calle_entre1

    def clean_calle_entre2(self):
        calle_entre2 = self.cleaned_data['calle_entre2']
        if calle_entre2:
            if not regex_alfanumerico.match(calle_entre2):
                raise forms.ValidationError('El nombre de la calle, solo puede contener letras/números y/o espacios')
        return calle_entre2

    def clean_dpto(self):
        dpto = self.cleaned_data['dpto']
        if dpto:
            if not regex_alfanumerico.match(dpto):
                raise forms.ValidationError('El Departamento, solo puede contener letras/números y/o espacios')
        return dpto


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
