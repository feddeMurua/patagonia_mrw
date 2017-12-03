# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from django.utils import timezone
from desarrollo_patagonia.utils import *
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin
from django.db.models import Sum

'''
MOVIMIENTO DIARIO
'''


class AltaFactura(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = MovimientoDiario
    fields = ['titular', 'nro_ingreso', 'forma_pago', 'nro_cheque']
    template_name = "caja/factura_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def lista_movimientos(request):
    movimientos = MovimientoDiario.objects.filter(fecha=timezone.now().date()).order_by('nro_ingreso')
    fecha_form = DatePickerForm
    if request.method == 'POST':
        fecha_form = DatePickerForm(request.POST)
        if fecha_form.is_valid():
            movimientos = MovimientoDiario.objects.filter(fecha=fecha_form.cleaned_data['fecha']).order_by('nro_ingreso')
    return render(request, 'caja/caja_list.html', {'listado': movimientos, 'fecha_form': fecha_form})


def get_total(detalles):
    total = 0
    for detalle in detalles:
        total += detalle.servicio.importe
    return total


@login_required(login_url='login')
def detalle_movimiento(request, pk):
    movimiento = MovimientoDiario.objects.get(pk=pk)
    detalles = DetalleMovimiento.objects.filter(movimiento=movimiento)
    total = get_total(detalles)
    return render(request, "caja/movimiento_detail.html", {'movimiento': movimiento, 'detalles': detalles,
                                                           'total': total})


'''
ARQUEO DIARIO DE CAJA
'''


@login_required(login_url='login')
def lista_arqueos(request):
    return render(request, 'arqueo/arqueo_list.html', {'listado': ArqueoDiario.objects.all()})


def get_ingresos_varios():
    movimientos = MovimientoDiario.objects.filter(fecha=timezone.now().date())
    debito_credito_cant = 0
    debito_credito_imp = 0
    cheque_cant = 0
    cheque_imp = 0
    efectivo_cant = 0
    efectivo_imp = 0
    if movimientos:
        for movimiento in movimientos:
            if movimiento.forma_pago != 'Eximido':
                importe = DetalleMovimiento.objects.filter(movimiento=movimiento).aggregate(Sum('servicio__importe'))
                if movimiento.forma_pago == 'Debito' or movimiento.forma_pago == 'Credito':
                    debito_credito_cant += 1
                    debito_credito_imp += importe['servicio__importe__sum']
                elif movimiento.forma_pago == 'Cheque':
                    cheque_cant += 1
                    cheque_imp += importe['servicio__importe__sum']
                else:
                    efectivo_cant += 1
                    efectivo_imp += importe['servicio__importe__sum']
    return {'debito_credito_cant': debito_credito_cant, 'debito_credito_imp': debito_credito_imp,
            'cheque_cant': cheque_cant, 'cheque_imp': cheque_imp, 'efectivo_cant': efectivo_cant,
            'efectivo_imp': efectivo_imp}


@login_required(login_url='login')
def alta_arqueo(request):
    ingresos_varios = get_ingresos_varios()
    if request.method == 'POST':
        form = ArqueoDiarioEfectivoForm(request.POST)
        form_otros = ArqueoDiarioOtrosForm(request.POST)
        if form.is_valid() & form_otros.is_valid():
            arqueo = form.save(commit=False)
            request.session['datos'] = arqueo.to_json_datos()
            request.session['dinero'] = arqueo.to_json_dinero()
            return redirect('arqueo:resumen_alta_arqueo')
    else:
        form = ArqueoDiarioEfectivoForm
        form_otros = ArqueoDiarioOtrosForm
    return render(request, 'arqueo/arqueo_form.html', {'form': form, 'form_otros': form_otros,
                                                       'ingresos_varios': ingresos_varios})


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
