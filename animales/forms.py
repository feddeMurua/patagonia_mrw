# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext as _
from functools import partial
from .models import *
from .choices import *
import re
import datetime
from django.utils import timezone
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.urlresolvers import reverse_lazy

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

regex_alfabetico = re.compile(r"^[a-zñA-ZÑ]+((\s[a-zñA-ZÑ]+)+)?$")
regex_alfanumerico = re.compile(r"^[a-zñA-ZÑ0-9]+((\s[a-zñA-ZÑ0-9]+)+)?$")


class AltaAnalisisForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = Analisis
        exclude = ['medico_veterinario', 'resultado']
        fields = '__all__'
        widgets = {
            'procedencia': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_localidad'),
            )
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return fecha


class ModificacionAnalisisForm(forms.ModelForm):

    class Meta:
        model = Analisis
        fields = ['procedencia', 'categoria']
        widgets = {
            'procedencia': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('personas:nueva_localidad'),
            )
        }


class ResultadoAnalisisForm(forms.ModelForm):
    medico_veterinario = forms.ModelChoiceField(queryset=m.PersonalPropio.objects.filter(
        rol_actuante__nombre='Medico'), required=False)

    class Meta:
        model = Analisis
        fields = ['medico_veterinario', 'resultado']


class PorcinoForm(forms.ModelForm):

    class Meta:
        model = Porcino
        fields = ['precinto', 'categoria_porcino']
        labels = {
            'categoria_porcino': _("Categoria del porcino")
        }


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

    def clean_fecha_disposicion(self):
        fecha_disposicion = self.cleaned_data['fecha_disposicion']
        if fecha_disposicion > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return fecha_disposicion


class MascotaForm(forms.ModelForm):
    nacimiento_fecha = forms.DateField(widget=DateInput(), label="Fecha de nacimiento", required=False)

    class Meta:
        model = Mascota
        exclude = ['baja', 'esterilizado']
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

    def clean_nacimiento_fecha(self):
        nacimiento_fecha = self.cleaned_data['nacimiento_fecha']
        if nacimiento_fecha and nacimiento_fecha > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return nacimiento_fecha


class PatenteForm(forms.ModelForm):

    class Meta:
        model = Patente
        fields = ['nro_patente', 'persona', 'observaciones']
        labels = {
            'nro_patente': _("N° de patente"),

        }
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }

    def __init__(self, *args, **kwargs):
        self.categoria = kwargs.pop('categoria', None)
        super(PatenteForm, self).__init__(*args, **kwargs)

    def clean_nro_patente(self):
        nro_patente = self.cleaned_data['nro_patente']
        patentes = Patente.objects.filter(mascota__categoria_mascota=self.categoria).values_list('nro_patente', flat=True)
        if nro_patente in patentes:
            raise forms.ValidationError(_('Ya existe una patente con este número'), code='invalid')
        return nro_patente


class ModificacionPatenteForm(forms.ModelForm):

    class Meta:
        model = Patente
        fields = ['nro_patente', 'persona', 'observaciones']
        labels = {
            'nro_patente': _("N° de patente"),

        }

    def clean_nro_patente(self):
        nro_patente = self.cleaned_data['nro_patente']
        patentes = Patente.objects.filter(mascota__categoria_mascota=self.instance.mascota.categoria_mascota).values_list('nro_patente', flat=True)
        if nro_patente in patentes:
            raise forms.ValidationError(_('Ya existe una patente con este número'), code='invalid')
        return nro_patente


class ControlAntirrabicoForm(forms.ModelForm):
    fecha_suceso = forms.DateField(widget=DateInput(), label="Fecha del suceso")

    class Meta:
        model = ControlAntirrabico
        fields = '__all__'
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20})
        }
        labels = {
            'responsable': _("Responsable del animal"),

        }

    def clean_fecha_suceso(self):
        fecha_suceso = self.cleaned_data['fecha_suceso']
        if fecha_suceso > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return fecha_suceso


class VisitaForm(forms.ModelForm):
    fecha_visita = forms.DateField(widget=DateInput(), label="Fecha de la visita")

    class Meta:
        model = Visita
        exclude = ['control']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        self.control = kwargs.pop('control', None)
        super(VisitaForm, self).__init__(*args, **kwargs)

    def clean_fecha_visita(self):
        fecha_visita = self.cleaned_data['fecha_visita']
        if fecha_visita < self.control.fecha_suceso:
            raise forms.ValidationError('La fecha seleccionada no puede ser anterior a la fecha del suceso')
        else:
            visitas = Visita.objects.filter(control=self.control, fecha_visita=fecha_visita).last()
            if visitas:
                raise forms.ValidationError('Ya existe una visita registrada en esa fecha')
        return fecha_visita


class RetiroEntregaForm(forms.ModelForm):

    class Meta:
        model = RetiroEntregaAnimal
        fields = ['tramite', 'observaciones', 'patentado']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        }


class ModificacionRetiroEntregaForm(forms.ModelForm):

    class Meta:
        model = RetiroEntregaAnimal
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        }


class ListaPatentesForm(forms.Form):
    patente = forms.ModelChoiceField(queryset=Patente.objects.all(), required=True)


class ListaPatentesEsterilizacionForm(forms.Form):
    patente = forms.ModelChoiceField(queryset=Patente.objects.filter(mascota__esterilizado=False), required=True)


class EsterilizacionPatenteForm(forms.ModelForm):
    ultimo_celo = forms.DateField(widget=DateInput(), required=False)

    class Meta:
        model = Esterilizacion
        exclude = ['interesado', 'mascota']
        labels = {
            'anticonceptivos': _("Cantidad de anticonceptivos aplicados"),
            'partos': _("Cantidad de partos"),
        }

    def clean_ultimo_celo(self):
        ultimo_celo = self.cleaned_data['ultimo_celo']
        if ultimo_celo and ultimo_celo > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return ultimo_celo

    def clean_turno(self):
        turno = self.cleaned_data['turno']
        if turno.time() < datetime.time(8, 0) or turno.time() > datetime.time(20, 0):
            raise forms.ValidationError('Debe seleccionar un horario entre las 08:00 y las 20:00 hs.')
        elif turno.date() < timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser menor a la fecha actual')
        return turno


class EsterilizacionNuevoForm(forms.ModelForm):
    ultimo_celo = forms.DateField(widget=DateInput(), required=False)

    class Meta:
        model = Esterilizacion
        exclude = ['mascota']
        labels = {
            'anticonceptivos': _("Cantidad de anticonceptivos aplicados"),
            'partos': _("Cantidad de partos"),
        }

    def clean_ultimo_celo(self):
        ultimo_celo = self.cleaned_data['ultimo_celo']
        if ultimo_celo and ultimo_celo > timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser mayor a la fecha actual')
        return ultimo_celo

    def clean_turno(self):
        turno = self.cleaned_data['turno']
        if turno.time() < datetime.time(8, 0) or turno.time() > datetime.time(12, 0):
            raise forms.ValidationError('Debe seleccionar un horario entre las 08:00 y las 12:00 hs.')
        elif turno.date() < timezone.now().date():
            raise forms.ValidationError('La fecha seleccionada no puede ser menor a la fecha actual')
        return turno
