# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .filters import *
# Create your views here.

'''
MOVIMIENTO DIARIO
'''

@login_required(login_url='login')
def lista_detalle_movimientos(request):
    detalle_movimientos = DetalleMovimiento.objects.all()
    filtro_detalle_movimientos = DetalleMovimientoListFilter(request.GET, queryset=detalle_movimientos)
    return render(request, 'caja/caja_list.html', {'filter': filtro_detalle_movimientos})
