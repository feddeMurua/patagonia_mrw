# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.contrib.admin.models import LogEntry
from django.shortcuts import render
from .forms import *
from personas import forms as pf
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required(login_url='login')
@staff_member_required
def lista_eventos(request):
    eventos = LogEntry.objects.filter(action_time__gt=datetime.now() - timedelta(days=1))
    rango_form = RangoEventosForm
    if request.method == 'POST':
        rango_form = RangoEventosForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']
            eventos = LogEntry.objects.filter(action_time__gt=fecha_desde, action_time__lt=fecha_hasta)
    return render(request, 'eventos/eventos_list.html', {'rango_form': rango_form, 'listado': eventos})
