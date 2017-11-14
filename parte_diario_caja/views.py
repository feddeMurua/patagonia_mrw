# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from django.utils import timezone
from desarrollo_patagonia.utils import *
from django.contrib.admin.views.decorators import staff_member_required

'''
MOVIMIENTO DIARIO
'''


@login_required(login_url='login')
def lista_detalle_movimientos(request):
    movimientos = DetalleMovimiento.objects.filter(movimiento__fecha=timezone.now().date()).order_by(
        'movimiento__nro_ingreso')
    fecha_form = DatePickerForm
    if request.method == 'POST':
        fecha_form = DatePickerForm(request.POST)
        if fecha_form.is_valid():
            movimientos = DetalleMovimiento.objects.filter(movimiento__fecha=fecha_form.cleaned_data['fecha']).order_by(
                'movimiento__nro_ingreso')
    return render(request, 'caja/caja_list.html', {'listado': movimientos, 'fecha_form': fecha_form})


'''
ARQUEO DIARIO DE CAJA
'''


@login_required(login_url='login')
def lista_arqueos(request):
    return render(request, 'arqueo/arqueo_list.html', {'listado': ArqueoDiario.objects.all()})


def get_ingresos_varios():
    movimientos = DetalleMovimiento.objects.filter(movimiento__fecha=timezone.now().date())
    debito_credito = [0, 0]
    cheque = [0, 0]
    efectivo = 0
    if movimientos:
        for movimiento in movimientos:
            if movimiento.forma_pago != 'Eximido':
                if movimiento.forma_pago == ('Debito' or 'Credito'):
                    debito_credito[0] += 1
                    debito_credito[1] += movimiento.servicio.importe
                elif movimiento.forma_pago == 'Cheque':
                    cheque[0] += 1
                    cheque[1] += movimiento.servicio.importe
                else:
                    efectivo += movimiento.servicio.importe
    return {'debito_credito': debito_credito, 'cheque': cheque, 'efectivo': efectivo}


@login_required(login_url='login')
def alta_arqueo(request):
    if request.method == 'POST':
        form = ArqueoDiarioEfectivoForm(request.POST)
        form_otros = ArqueoDiarioOtrosForm(request.POST)
        ingresos_varios = get_ingresos_varios()
        if form.is_valid() & form_otros.is_valid():
            arqueo = form.save(commit=False)
            request.session['datos'] = arqueo.to_json_datos()
            request.session['dinero'] = arqueo.to_json_dinero()
            return redirect('arqueo:resumen_alta_arqueo')
    else:
        form = ArqueoDiarioEfectivoForm
        form_otros = ArqueoDiarioOtrosForm
    return render(request, 'arqueo/arqueo_form.html', {'form': form, 'form_otros': form_otros})


@staff_member_required
@login_required(login_url='login')
def lista_servicios(request):
    return render(request, 'servicio/servicio_list.html', {'listado': Servicio.objects.all()})


@staff_member_required
@login_required(login_url='login')
def alta_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Servicio')
            return redirect('servicios:lista_servicios')
    else:
        form = ServicioForm
    return render(request, 'servicio/servicio_form.html', {'form': form})


@staff_member_required
@login_required(login_url='login')
def baja_servicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    log_eliminar(request.user.id, servicio, 'Servicio')
    servicio.delete()
    return HttpResponse()


@staff_member_required
@login_required(login_url='login')
def modificacion_servicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Servicio')
            return redirect('servicios:lista_servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'servicio/servicio_form.html', {'form': form})
