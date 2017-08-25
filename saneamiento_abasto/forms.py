# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from functools import partial
import re
from .models import *


class AbastecedorForm(forms.ModelForm):

    class Meta:
        model = Abastecedor
        fields = ['persona', 'empresa_y_o_transporte', 'rubro']
