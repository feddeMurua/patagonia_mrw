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
from desarrollo_patagonia import forms as dp_f
import collections
import json

'''
MOVIMIENTO DIARIO
'''


class AltaFactura(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = MovimientoDiario
    form_class = MovimientoDiarioForm
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
        total += detalle.importe
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
    arqueos = ArqueoDiario.objects.all()
    if not arqueos:
        realizado = False
    else:
        realizado = True if arqueos.last().fecha == timezone.now().date() else False
    return render(request, 'arqueo/arqueo_list.html', {'listado': arqueos, 'realizado': realizado})


def get_ingresos_varios():
    movimientos = MovimientoDiario.objects.filter(fecha=timezone.now().date())
    tarjeta_mov = 0
    tarjeta_imp = 0
    cheque_mov = 0
    cheque_imp = 0
    efectivo_mov = 0
    efectivo_imp = 0
    total_mov = 0
    total_imp = 0
    if movimientos:
        for movimiento in movimientos:
            if movimiento.forma_pago != 'Eximido':
                importe = DetalleMovimiento.objects.filter(movimiento=movimiento).aggregate(Sum('importe'))
                if movimiento.forma_pago == 'Debito' or movimiento.forma_pago == 'Credito':
                    tarjeta_mov += 1
                    tarjeta_imp += importe['importe__sum']
                elif movimiento.forma_pago == 'Cheque':
                    cheque_mov += 1
                    cheque_imp += importe['importe__sum']
                else:
                    efectivo_mov += 1
                    efectivo_imp += importe['importe__sum']
        total_mov = tarjeta_mov + cheque_mov + efectivo_mov
        total_imp = tarjeta_imp + cheque_imp + efectivo_imp
    return {'tarjeta_mov': tarjeta_mov, 'tarjeta_imp': tarjeta_imp, 'cheque_mov': cheque_mov, 'cheque_imp': cheque_imp,
            'efectivo_mov': efectivo_mov, 'efectivo_imp': efectivo_imp, 'total_mov': total_mov, 'total_imp': total_imp}


@login_required(login_url='login')
def alta_arqueo(request):
    ingresos_varios = get_ingresos_varios()
    if request.method == 'POST':
        form = ArqueoEfectivoForm(request.POST)
        form_otros = ArqueoOtrosForm(request.POST)
        if form.is_valid() & form_otros.is_valid():
            datos = {}
            datos.update(form.cleaned_data)
            datos.update(form_otros.cleaned_data)
            arqueo = ArqueoDiario.objects.create(**datos)
            arqueo.total_manual = request.POST['total_manual']
            arqueo.detalle_sistema(ingresos_varios)
            log_crear(request.user.id, arqueo, 'Arqueo diario de caja')
            return redirect('arqueo:lista_arqueos')
    else:
        form = ArqueoEfectivoForm
        form_otros = ArqueoOtrosForm
    return render(request, 'arqueo/arqueo_form.html', {'form': form, 'form_otros': form_otros,
                                                       'ingresos_varios': ingresos_varios})


@login_required(login_url='login')
def detalle_arqueo(request, pk):
    return render(request, 'arqueo/arqueo_detail.html', {'arqueo': ArqueoDiario.objects.get(pk=pk)})


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


@login_required(login_url='login')
def estadisticas_caja(request):
    rango_form = dp_f.RangoFechaForm
    years = [2018]
    if request.method == 'POST':
        rango_form = dp_f.RangoFechaForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']
            anio_desde = fecha_desde.year
            anio_hasta = fecha_hasta.year
            years = range(anio_hasta, anio_desde - 1, -1)

    importe_anual = {}  # importe anual POR SERVICIO

    for year in years:
        movimientos_caja = MovimientoDiario.objects.filter(fecha__year=year)
        for mov in movimientos_caja:
            for detalle in DetalleMovimiento.objects.filter(movimiento=mov):
                importe_anual[detalle.servicio] = (DetalleMovimiento.objects.filter(movimiento__fecha__year=year, servicio=detalle.servicio).count())*detalle.importe

    total_general = sum(importe_anual.values())  # Total generado en el año

    ord_importe_anual = collections.OrderedDict(sorted(importe_anual.iteritems(), key=lambda (k, v): (v, k)))  # Ordena los servicios por importe

    label_servicios = ord_importe_anual.keys()  # indistinto para los datos (tienen la misma clave)
    datos_servicios = ord_importe_anual.values()

    porcentajes = []
    for v in ord_importe_anual.values():
        porcentajes.append(float("{0:.2f}".format(v*100/total_general)))

    context = {
        'rango_form': rango_form,
        'dict': ord_importe_anual,
        'porcentajes': porcentajes,
        'total_general': total_general,
        # datos y etiquetas
        'lista_labels': json.dumps([label_servicios]),
        'lista_datos': json.dumps([{'Servicios': datos_servicios}])
    }

    return render(request, "estadistica/estadisticas_caja.html", context)
