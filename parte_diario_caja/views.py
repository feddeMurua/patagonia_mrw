# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from .forms import *
from django.utils import timezone
from desarrollo_patagonia.utils import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from desarrollo_patagonia import forms as dp_f
from dateutil.relativedelta import *
import collections
import json
import datetime
from weasyprint import HTML
from django.template.loader import get_template

'''
MOVIMIENTO DIARIO
'''


@login_required(login_url='login')
def lista_movimientos(request):
    movimientos = MovimientoDiario.objects.filter(fecha=timezone.now().date()).order_by('nro_ingreso')
    fecha_form = DatePickerForm
    if request.method == 'POST':
        fecha_form = DatePickerForm(request.POST)
        if fecha_form.is_valid():
            if request.POST.get("buscar"):
                movimientos = MovimientoDiario.objects.filter(fecha=fecha_form.cleaned_data['fecha']).order_by(
                    'nro_ingreso')
            elif request.POST.get("imprimir"):
                fecha = fecha_form.cleaned_data['fecha']
                return HttpResponseRedirect(reverse('caja:parte_diario_pdf',
                                                    kwargs={'anio': fecha.year, 'mes': fecha.month, 'dia': fecha.day}))
    return render(request, 'caja/caja_list.html', {'listado': movimientos, 'fecha_form': fecha_form})


@login_required(login_url='login')
def detalle_movimiento(request, pk):
    movimiento = MovimientoDiario.objects.get(pk=pk)
    detalles = DetalleMovimiento.objects.filter(movimiento=movimiento)
    return render(request, "caja/movimiento_detail.html", {'movimiento': movimiento, 'detalles': detalles,
                                                           'total': sum(detalle.importe for detalle in detalles)})


@login_required(login_url='login')
def modificar_movimiento(request, pk):
    movimiento = MovimientoDiario.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificarMovimientoDiarioForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            log_modificar(request.user.id, movimiento, 'Movimiento Diario')
            return redirect('caja:lista_movimientos')
    else:
        form = ModificarMovimientoDiarioForm(instance=movimiento)
    return render(request, 'caja/modificar_movimiento.html', {'form': form})


@login_required(login_url='login')
def modificar_detalle(request, pk):
    detalle = DetalleMovimiento.objects.get(pk=pk)
    if request.method == 'POST':
        form = DetalleMovimientoDiarioForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            log_modificar(request.user.id, detalle, 'Detalle de Movimiento Diario')
            return redirect('caja:lista_movimientos')
    else:
        form = DetalleMovimientoDiarioForm(instance=detalle)
    return render(request, 'caja/modificar_detalle.html', {'pk_mov': detalle.movimiento.pk, 'form': form})


@login_required(login_url='login')
def verificar_nro_ingreso(request):
    existe = False
    try:
        MovimientoDiario.objects.get(nro_ingreso=request.GET['nro_ingreso'])
        existe = True
    except:
        pass
    return JsonResponse({'existe': existe})


def movimiento_previo(request, form, servicio, obj, logname):
    detalle_mov = form.save(commit=False)
    detalle_mov.completar(Servicio.objects.get(nombre=servicio), obj)
    log_crear(request.user.id, obj, logname)


def nuevo_movimiento(request, form, servicio, obj, logname):
    mov = form.save()
    detalle_mov = DetalleMovimiento(movimiento=mov)
    detalle_mov.completar(Servicio.objects.get(nombre=servicio), obj)
    log_crear(request.user.id, obj, logname)


def get_subtotales(detalles):
    movimientos = MovimientoDiario.objects.filter(fecha=timezone.now().date())
    subtotales = {'efectivo': 0, 'tarjeta': 0, 'cheque': 0, 'total': 0}
    for movimiento in movimientos:
        if movimiento.forma_pago != 'Eximido':
            detalles_movimiento = detalles.filter(movimiento=movimiento)
            sub = sum(detalle.importe for detalle in detalles_movimiento)
            if movimiento.forma_pago == 'Efectivo':
                subtotales['efectivo'] += sub
            elif movimiento.forma_pago == 'Tarjeta':
                subtotales['tarjeta'] += sub
            else:
                subtotales['cheque'] += sub
            subtotales['total'] += sub
    return subtotales


@login_required(login_url='login')
def pdf_parte_diario(request, anio, mes, dia):
    template = get_template('caja/parte_diario_pdf.html')
    fecha = datetime.date(int(anio), int(mes), int(dia))
    detalles = DetalleMovimiento.objects.filter(movimiento__fecha=fecha).order_by('movimiento__nro_ingreso')
    subtotales = get_subtotales(detalles)
    context = {'title': 'Parte diario del dia ' + str(fecha.strftime('%d/%m/%Y')), 'detalles': detalles,
               'subtotales': subtotales, 'fecha_maniana': fecha + relativedelta(days=1)}
    rendered = template.render(context)
    pdf_file = HTML(string=rendered, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' + str("Parte_diario_dia_" + str(fecha.strftime('%d/%m/%Y')))
    return response


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
    subtotales = {'tarjeta_mov': 0, 'tarjeta_imp': 0, 'cheque_mov': 0, 'cheque_imp': 0, 'efectivo_mov': 0,
                  'efectivo_imp': 0, 'total_mov': 0, 'total_imp': 0}
    if movimientos:
        for movimiento in movimientos:
            if movimiento.forma_pago != 'Eximido':
                importe = DetalleMovimiento.objects.filter(movimiento=movimiento).aggregate(Sum('importe'))
                if movimiento.forma_pago == 'Tarjeta':
                    subtotales['tarjeta_mov'] += 1
                    subtotales['tarjeta_imp'] += importe['importe__sum']
                elif movimiento.forma_pago == 'Cheque':
                    subtotales['cheque_mov'] += 1
                    subtotales['cheque_imp'] += importe['importe__sum']
                else:
                    subtotales['efectivo_mov'] += 1
                    subtotales['efectivo_imp'] += importe['importe__sum']
        subtotales['total_mov'] = subtotales['tarjeta_mov'] + subtotales['cheque_mov'] + subtotales['efectivo_mov']
        subtotales['total_imp'] = subtotales['tarjeta_imp'] + subtotales['cheque_imp'] + subtotales['efectivo_imp']
    return subtotales


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


def calculo_arqueo(arqueo):
    return {'mil': arqueo.mil, 'quinientos': arqueo.quinientos * 500, 'doscientos': arqueo.doscientos * 200,
            'cien': arqueo.cien * 100, 'b_cincuenta': arqueo.b_cincuenta * 50, 'veinte': arqueo.veinte * 20,
            'diez': arqueo.diez * 10, 'cinco': arqueo.cinco * 5, 'm_dos': arqueo.m_dos * 2, 'uno': arqueo.uno,
            'm_cincuenta': arqueo.m_cincuenta * 0.50, 'veinticinco': arqueo.veinticinco * 0.25, 'arqueo': arqueo}


@login_required(login_url='login')
def detalle_arqueo(request, pk):
    return render(request, 'arqueo/arqueo_detail.html', {'datos': calculo_arqueo(ArqueoDiario.objects.get(pk=pk))})


@login_required(login_url='login')
def pdf_arqueo(request, planilla):
    template = get_template('arqueo/arqueo_pdf.html')
    arqueo = ArqueoDiario.objects.get(nro_planilla=planilla)
    context = {'datos': calculo_arqueo(arqueo),
               'title': 'Arqueo de efectivo del dia ' + str(arqueo.fecha.strftime('%d/%m/%Y') + ' / N° de planilla')}
    rendered = template.render(context)
    pdf_file = HTML(string=rendered, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' + str("Arqueo_caja_" + str(arqueo.fecha.strftime('%d/%m/%Y')))
    return response


'''
SERVICIOS
'''


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


'''
ESTADISTICAS
'''


@login_required(login_url='login')
def estadisticas_caja(request):
    rango_form = dp_f.RangoFechaForm
    fecha_desde = timezone.now() - relativedelta(years=1)
    fecha_hasta = timezone.now()
    if request.method == 'POST':
        rango_form = dp_f.RangoFechaForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']

    importe_total = {}

    movimientos = MovimientoDiario.objects.filter(fecha__gte=fecha_desde, fecha__lte=fecha_hasta)
    for mov in movimientos:
        for detalle in DetalleMovimiento.objects.filter(movimiento=mov):
            importe_total[detalle.servicio] = (DetalleMovimiento.objects.filter(servicio=detalle.servicio).count()) * detalle.importe

    total_general = sum(importe_total.values())  # Total generado en el año
    ord_importe_anual = collections.OrderedDict(
        sorted(importe_total.iteritems(), key=lambda (k, v): (k, v)))  # Ordena los servicios por importe
    label_servicios = ord_importe_anual.keys()  # indistinto para los datos (tienen la misma clave)
    datos_servicios = ord_importe_anual.values()

    for k, v in ord_importe_anual.items():
        ord_importe_anual[k] = (v, float("{0:.2f}".format(v * 100 / total_general)))

    context = {
        'rango_form': rango_form,
        'dict': ord_importe_anual,
        'total_general': total_general,
        # datos y etiquetas
        'lista_labels': json.dumps([label_servicios]),
        'lista_datos': json.dumps([{'Servicios': datos_servicios}])
    }
    return render(request, "estadistica/estadisticas_caja.html", context)
