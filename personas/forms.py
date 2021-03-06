# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from usuarios.models import CustomUser
from django import forms
from functools import partial
import re
from django.utils.translation import ugettext as _
from .models import *
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

regex_alfabetico = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")
regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class ListaUsuariosForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=CustomUser.objects.all())


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


class AltaPersonaFisicaForm(PersonaGenericaForm):
    fecha_nacimiento = forms.DateField(widget=DateInput(), label="Fecha de nacimiento")

    class Meta:
        model = PersonaFisica
        fields = ['apellido', 'nombre', 'nacionalidad', 'tipo_dni', 'dni', 'fecha_nacimiento', 'telefono', 'email',
                  'obra_social']
        labels = {
            'tipo_dni': _("Tipo de documento"),
            'dni': _("Documento")
        }
        widgets = {
            'nacionalidad': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_nacionalidad'),
            )
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not regex_alfabetico.match(nombre):
            raise forms.ValidationError('El nombre de la persona, solo puede contener letras y/o espacios')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not regex_alfabetico.match(apellido):
            raise forms.ValidationError('El apellido de la persona, solo puede contener letras y/o espacios')
        return apellido

    def clean_obra_social(self):
        obra_social = self.cleaned_data['obra_social']
        if obra_social:
            if not regex_alfanumerico.match(obra_social):
                raise forms.ValidationError('La obra social solo puede contener letras, numeros y/o espacios')
        return obra_social

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser menor a la fecha actual')
        return fecha_nacimiento


class ModificacionPersonaFisicaForm(forms.ModelForm):

    class Meta:
        model = PersonaFisica
        fields = ['apellido', 'nombre', 'nacionalidad', 'tipo_dni', 'dni', 'fecha_nacimiento', 'telefono', 'email',
                  'obra_social', 'documentacion_retirada']
        labels = {
            'tipo_dni': _("Tipo de documento"),
            'dni': _("Documento")
        }
        widgets = {
            'nacionalidad': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_nacionalidad'),
            )
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not regex_alfabetico.match(nombre):
            raise forms.ValidationError('El nombre de la persona, solo puede contener letras y/o espacios')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not regex_alfabetico.match(apellido):
            raise forms.ValidationError('El apellido de la persona, solo puede contener letras y/o espacios')
        return apellido

    def clean_obra_social(self):
        obra_social = self.cleaned_data['obra_social']
        if obra_social:
            if not regex_alfanumerico.match(obra_social):
                raise forms.ValidationError('La obra social solo puede contener letras, numeros y/o espacios')
        return obra_social

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser menor a la fecha actual')
        return fecha_nacimiento


class AltaPersonaJuridicaForm(forms.ModelForm):

    class Meta:
        model = PersonaJuridica
        exclude = ['domicilio']
        labels = {
            'nombre': _("Razon social")
        }


class ModificacionPersonaJuridicaForm(forms.ModelForm):

    class Meta:
        model = PersonaJuridica
        exclude = ['domicilio']
        labels = {
            'nombre': _("Razon social")
        }


class PersonalPropioForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput(), label="Fecha de nacimiento")

    class Meta:
        model = PersonalPropio
        fields = ['apellido', 'nombre', 'nacionalidad', 'tipo_dni', 'dni', 'fecha_nacimiento', 'telefono', 'email',
                  'obra_social', 'rol_actuante']
        labels = {
            'tipo_dni': _("Tipo de documento"),
            'dni': _("Documento")
        }
        widgets = {
            'nacionalidad': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_nacionalidad'),
            )
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not regex_alfabetico.match(nombre):
            raise forms.ValidationError('El nombre de la persona, solo puede contener letras y/o espacios')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not regex_alfabetico.match(apellido):
            raise forms.ValidationError('El apellido de la persona, solo puede contener letras y/o espacios')
        return apellido

    def clean_obra_social(self):
        obra_social = self.cleaned_data['obra_social']
        if obra_social:
            if not regex_alfanumerico.match(obra_social):
                raise forms.ValidationError('La obra social solo puede contener letras, numeros y/o espacios')
        return obra_social

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada debe ser menor a la fecha actual')
        return fecha_nacimiento


class DomicilioForm(forms.ModelForm):

    class Meta:
        model = Domicilio
        fields = '__all__'
        widgets = {
            'localidad': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_localidad'),
            )
        }


class DomicilioRuralForm(forms.ModelForm):

    class Meta:
        model = DomicilioRural
        fields = '__all__'

    def clean_chacra(self):
        chacra = self.cleaned_data['chacra']
        if chacra:
            if not regex_alfanumerico.match(chacra):
                raise forms.ValidationError('La Chacra, solo puede contener letras/números y/o espacios')
        return chacra

    def clean_parcela(self):
        parcela = self.cleaned_data['parcela']
        if parcela:
            if not regex_alfanumerico.match(parcela):
                raise forms.ValidationError('La Parcela, solo puede contener letras/números y/o espacios')
        return parcela

    def clean_sector(self):
        sector = self.cleaned_data['sector']
        if sector:
            if not regex_alfanumerico.match(sector):
                raise forms.ValidationError('El sector, solo puede contener letras/números y/o espacios')
        return sector

    def clean_circunscripcion(self):
        circunscripcion = self.cleaned_data['circunscripcion']
        if circunscripcion:
            if not regex_alfanumerico.match(circunscripcion):
                raise forms.ValidationError('La Circunscripcion, solo puede contener letras/números y/o espacios')
        return circunscripcion

    def clean_ruta(self):
        ruta = self.cleaned_data['ruta']
        if ruta:
            if not regex_alfanumerico.match(ruta):
                raise forms.ValidationError('La Ruta, solo puede contener letras/números y/o espacios')
        return ruta


class LocalidadForm(forms.ModelForm):

    class Meta:
        model = Localidad
        fields = '__all__'
        labels = {
            'cp': _("Código postal")
        }
        widgets = {
            'provincia': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_provincia'),
            )
        }

    def clean(self):
        cleaned_data = super(LocalidadForm, self).clean()
        nombre = cleaned_data.get("nombre")
        provincia = cleaned_data.get("provincia")
        if nombre and provincia:
            if Localidad.objects.filter(nombre__iexact=nombre, provincia=provincia).last():
                self.add_error('nombre', forms.ValidationError('La localidad ingresada ya se encuentra registrada en el'
                                                               'sistema para la provincia seleccionada'))


class ProvinciaForm(forms.ModelForm):

    class Meta:
        model = Provincia
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ProvinciaForm, self).clean()
        nombre = cleaned_data.get("nombre")
        nacionalidad = cleaned_data.get("nacionalidad")
        if nombre and nacionalidad:
            if Provincia.objects.filter(nombre__iexact=nombre, nacionalidad=nacionalidad).last():
                self.add_error('nombre', forms.ValidationError('La provincia ingresada ya se encuentra registrada en el'
                                                               'sistema para el pais seleccionado'))


class NacionalidadForm(forms.ModelForm):

    class Meta:
        model = Nacionalidad
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if Nacionalidad.objects.filter(nombre__iexact=nombre).last():
            raise forms.ValidationError('El pais ingresado ya se encuentra registrado en el sistema')
        return nombre
