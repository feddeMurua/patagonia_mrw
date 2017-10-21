# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *
from datetime import datetime

'''
MOVIMIENTO DIARIO
'''


@login_required(login_url='login')
def lista_detalle_movimientos(request):
    fecha_busqueda = datetime.date(now())
    if request.method == 'POST':
        fecha_form = DatePickerForm(request.POST)
        if fecha_form.is_valid():
            fecha_busqueda = fecha_form.cleaned_data['fecha']
    movimientos = DetalleMovimiento.objects.filter(movimiento__fecha=fecha_busqueda).order_by('movimiento__nro_ingreso')
    datepicker = DatePickerForm
    return render(request, 'caja/caja_list.html', {'listado': movimientos, 'datepicker': datepicker})
