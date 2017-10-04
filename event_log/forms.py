# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms


class RangoEventosForm(forms.Form):
    fecha_desde = forms.DateTimeField(label='Fecha desde', required=True)
    fecha_hasta = forms.DateTimeField(label='Fecha hasta', required=True)
