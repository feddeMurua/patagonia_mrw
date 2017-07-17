from django import forms
from functools import partial
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class PersonaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'cuil', 'fecha_nacimiento', 'dni', 'nacionalidad', 'obra_social',
                  'domicilio', 'telefono', 'email', 'rubro']


class ExamenForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput())

    class Meta:
        model = ExamenClinico
        fields = "__all__"


class CursoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput())

    class Meta:
        model = Curso
        fields = ['fecha_inicio', 'cupo', 'lugar', 'horario']
        labels = {
            'fecha_inicio': _('Fecha de Inicio'),
            'cupo': _('Cupo'),
            'lugar': _('Lugar'),
            'horario': _('Horario')
        }
