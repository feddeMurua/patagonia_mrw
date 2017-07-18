from django import forms
from functools import partial
from .models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})


class PersonaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateInput())

    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'cuil', 'fecha_nacimiento', 'dni', 'nacionalidad', 'obra_social',
                  'domicilio', 'telefono', 'email', 'rubro']


class CursoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput())
    horario = forms.TimeField(widget=TimeInput())

    class Meta:
        model = Curso
        fields = ['fecha_inicio', 'cupo', 'lugar', 'horario']


class LibretaForm(forms.ModelForm):
    fecha_examen_clinico = forms.DateField(widget=DateInput())

    class Meta:
        model = LibretaSanitaria
        fields = ['nro_ingresos_varios', 'arancel', 'persona', 'curso',
                    'observaciones', 'fecha_examen_clinico',
                    'profesional_examen_clinico', 'lugar_examen_clinico', 'foto']
