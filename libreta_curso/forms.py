from django import forms
from django.forms import ModelForm
from functools import partial
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class PersonaForm(ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'cuil', 'fecha_nacimiento', 'dni', 'nacionalidad', 'obra_social',
                  'domicilio', 'telefono', 'email', 'rubro']


class CursoForm(ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput())

    class Meta:
        model = Curso
        fields = ['fecha_inicio', 'cupo', 'lugar', 'horario']


class LibretaForm(ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput())

    class Meta:
        model = LibretaSanitaria
        fields = ['nro_ingresos_varios', 'arancel','persona', 'curso',
                    'observaciones', 'fecha_examen_clinico',
                    'profesional_examen_clinico', 'lugar_examen_clinico', 'foto']
