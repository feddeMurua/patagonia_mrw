from django import forms
from django.forms import ModelForm
from functools import partial
from .models import (

    PersonaFisica,
    ExamenClinico,
    Curso

)


DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class PersonaForm(ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())
    class Meta:
        model = PersonaFisica
        fields = ['nombre','apellido', 'cuil', 'fecha_nacimiento', 'dni',
         'nacionalidad', 'obra_social','domicilio', 'telefono', 'email', 'rubro']


class ExamenForm(ModelForm):
    fecha = forms.DateField(widget=DateInput())
    class Meta:
        model = ExamenClinico
        fields = "__all__"


class CursoForm(ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput())
    class Meta:
        model = Curso
        fields = ['fecha_inicio', 'cupo', 'lugar', 'horario']
