# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from calendar import monthrange
from personas import forms as f
from .forms import *
from .choices import *
from parte_diario_caja import forms as pd_f
from parte_diario_caja import models as pd_m
from desarrollo_patagonia import forms as dp_f
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from desarrollo_patagonia.utils import *
from django.views.generic.detail import DetailView
from django.utils import timezone
from desarrollo_patagonia import factories
from libreta_curso import forms as lc_f
import collections
import numpy as np
import json


'''
ABASTECEDORES
'''


@login_required(login_url='login')
def lista_abastecedor(request):
    return render(request, 'abastecedor/abastecedor_list.html', {'listado': Abastecedor.objects.all()})


@login_required(login_url='login')
def alta_abastecedor(request):
    if request.method == 'POST':
        form = AbastecedorForm(request.POST)
        if form.is_valid():
            abastecedor = form.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor')
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = AbastecedorForm
    return render(request, 'abastecedor/abastecedor_form.html', {'form': form})


@login_required(login_url='login')
def nuevo_abastecedor_particular(request):
    if request.method == 'POST':
        form = f.AltaPersonaFisicaForm(request.POST)
        domicilio_form = f.DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            responsable = form.save(commit=False)
            responsable.domicilio = domicilio_form.save()
            responsable.save()
            abastecedor = Abastecedor(responsable=responsable)
            abastecedor.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor - Particular')
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = f.AltaPersonaFisicaForm
        domicilio_form = f.DomicilioForm
    return render(request, 'abastecedor/nuevo_abastecedor_form.html', {'form': form, 'domicilio_form': domicilio_form})


@login_required(login_url='login')
def nuevo_abastecedor_empresa(request):
    if request.method == 'POST':
        form = f.AltaPersonaJuridicaForm(request.POST)
        domicilio_form = f.DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            responsable = form.save(commit=False)
            responsable.domicilio = domicilio_form.save()
            responsable.save()
            abastecedor = Abastecedor(responsable=responsable)
            abastecedor.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor - Particular')
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = f.AltaPersonaJuridicaForm
        domicilio_form = f.DomicilioForm
    return render(request, 'abastecedor/nuevo_abastecedor_form.html', {'form': form, 'domicilio_form': domicilio_form})


@login_required(login_url='login')
def baja_abastecedor(request, pk):
    abastecedor = Abastecedor.objects.get(pk=pk)
    log_eliminar(request.user.id, abastecedor, 'Abastecedor')
    abastecedor.delete()
    return HttpResponse()


'''
CUENTAS CORRIENTES
'''


@login_required(login_url='login')
def lista_cc(request):
    return render(request, 'cuentaCorriente/cc_list.html', {'listado': CuentaCorriente.objects.all()})


@login_required(login_url='login')
def pagos_cc(request, pk):
    cuenta = CuentaCorriente.objects.get(pk=pk)
    return render(request, 'cuentaCorriente/cc_pagos_list.html', {'listado': PagoCC.objects.filter(cc=cuenta), 'cuenta': cuenta})


@login_required(login_url='login')
def realizar_pago_cc(request, pk):
    cuenta = CuentaCorriente.objects.get(pk=pk)
    if request.method == 'POST':
        form = PagoCCForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        if form.is_valid() & detalle_mov_form.is_valid():
            pago = form.save(commit=False)
            pago.cc = cuenta
            pago.save()
            cuenta.saldo -= pago.monto
            cuenta.save()
            detalle_mov = detalle_mov_form.save(commit=False)
            detalle_mov.importe = pago.monto
            detalle_mov.descripcion = 'Pago en Cuenta Corriente'
            detalle_mov.save()
            return HttpResponseRedirect(reverse('cuentas_corrientes:pagos_cc', kwargs={'pk': pk}))
    else:
        form = PagoCCForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
    return render(request, 'cuentaCorriente/cc_pago_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                                 'pk': pk})


@login_required(login_url='login')
def detalle_cc(request, pk):
    cuenta = CuentaCorriente.objects.get(pk=pk)
    detalles = DetalleCC.objects.filter(cc=cuenta)
    return render(request, 'cuentaCorriente/cc_detail.html', {'cuenta': cuenta, 'detalles': detalles})


'''
REINSPECCIONES
'''


@login_required(login_url='login')
def lista_reinspeccion(request):
    return render(request, 'reinspeccion/reinspeccion_list.html', {'listado': Reinspeccion.objects.all()})


@login_required(login_url='login')
def alta_reinspeccion(request):
    producto_form = ReinspeccionProductoForm
    if request.method == 'POST':
        form = ReinspeccionForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        if form.is_valid():
            reinspeccion = form.save()
            carga_productos(request, reinspeccion)
            monto = get_monto(reinspeccion)
            if request.POST['optradio'] == 'normal':
                if detalle_mov_form.is_valid():
                    detalle_mov = detalle_mov_form.save(commit=False)
                    detalle_mov.importe = monto
                    detalle_mov.descripcion = 'Reinspeccion Veterinaria'
                    detalle_mov.save()
            else:
                cc = CuentaCorriente.objects.get(abastecedor=reinspeccion.abastecedor)
                detalle = DetalleCC(detalle=reinspeccion, monto=monto, cc=cc)
                detalle.save()
                cc.saldo += monto
                cc.save()
            log_crear(request.user.id, reinspeccion, 'Reinspeccion')
            return redirect('reinspecciones:lista_reinspecciones')
    else:
        if 'productos' in request.session:
            del request.session['productos']
        request.session['productos'] = []
        form = ReinspeccionForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
    return render(request, 'reinspeccion/reinspeccion_form.html', {'form': form, 'producto_form': producto_form,
                                                                   'detalle_mov_form': detalle_mov_form})


def get_monto(reinspeccion):
    reinspeccion_prod = ReinspeccionProducto.objects.filter(reinspeccion=reinspeccion)
    precios = ReinspeccionPrecios.objects.get()

    total_kg = 0
    monto = precios.precio_min

    for r in reinspeccion_prod:
        total_kg += r.kilo_producto

    if total_kg > precios.kg_min:
        monto += total_kg * precios.precio_kg

    return monto


def existe_producto(request, producto):
    for item in request.session['productos']:
        if item['producto']['nombre'] == producto.producto.nombre:
            return True
    return False


@login_required(login_url='login')
def agregar_producto(request):
    form = ReinspeccionProductoForm(request.POST)
    success = True
    if form.is_valid():
        producto = form.save(commit=False)
        if existe_producto(request, producto):
            success = False
        else:
            request.session['productos'].append(producto.to_json())
            request.session.modified = True
    return JsonResponse({'success': success, 'productos': request.session['productos']})


@login_required(login_url='login')
def eliminar_producto(request, nombre):
    productos = request.session['productos']
    productos[:] = [p for p in productos if p.get('producto').get('nombre') != nombre]
    request.session['productos'] = productos
    return JsonResponse({'productos': request.session['productos']})


def carga_productos(request, reinspeccion):
    for producto in request.session['productos']:
        prod = Producto.objects.get(nombre=producto['producto']['nombre'])
        item = ReinspeccionProducto(producto=prod, kilo_producto=producto['kilo_producto'], reinspeccion=reinspeccion)
        item.save()


@login_required(login_url='login')
def lista_productos(request, reinspeccion_pk):
    return render(request, 'reinspeccion/producto_list.html', {'reinspeccion_pk': reinspeccion_pk,
                                                               'listado': ReinspeccionProducto.objects.filter(reinspeccion__pk=reinspeccion_pk)})


class AltaProducto(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = Producto
    form_class = AltaProductoForm
    template_name = "reinspeccion/simple_producto_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
@staff_member_required
def precios_reinspeccion(request):
    if request.method == 'POST':
        form = ReinspeccionPreciosForm(request.POST, instance=ReinspeccionPrecios.objects.get())
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Precios Reinspeccion')
            return redirect('reinspecciones:lista_reinspecciones')
    else:
        form = ReinspeccionPreciosForm(instance=ReinspeccionPrecios.objects.get())
    return render(request, 'reinspeccion/reinspeccion_precios.html', {'form': form})


'''
VEHICULO
'''


@login_required(login_url='login')
def get_rubros_json(request, id_categoria):
    return JsonResponse({
        'Categoria_A': CATEGORIA_A,
        'Categoria_B': CATEGORIA_B,
        'Categoria_C': CATEGORIA_C,
        'Categoria_D': CATEGORIA_D,
        'Categoria_E': CATEGORIA_E
    }.get(id_categoria, None))


@login_required(login_url='login')
def lista_vehiculo(request):
    return render(request, 'vehiculo/vehiculo_list.html', {'listado': Vehiculo.objects.all()})


class DetalleVehiculo(LoginRequiredMixin, DetailView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def alta_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            if vehiculo.categoria == 'TSA':
                vehiculo.rubro_vehiculo = request.POST['rubro_vehiculo']
            vehiculo.save()
            log_crear(request.user.id, vehiculo, 'Vehiculo')
            return redirect('vehiculo:lista_vehiculos')
    else:
        form = VehiculoForm
    return render(request, 'vehiculo/vehiculo_form.html', {'form': form})


@login_required(login_url='login')
def baja_vehiculo(request, pk):
    vehiculo = Vehiculo.objects.get(pk=pk)
    log_eliminar(request.user.id, vehiculo, 'Vehiculo')
    vehiculo.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_vehiculo(request, pk):
    vehiculo = Vehiculo.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificarTSAForm(request.POST, instance=vehiculo) if vehiculo.tipo_vehiculo == 'TSA'\
            else ModificarTPPForm(request.POST, instance=vehiculo)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.rubro_vehiculo = request.POST['rubro_vehiculo']
            vehiculo.save()
            log_modificar(request.user.id, vehiculo, 'Vehiculo')
            return redirect('vehiculo:lista_vehiculos')
    else:
        if vehiculo.tipo_vehiculo == 'TSA':
            form = ModificarTSAForm(instance=vehiculo)
            return render(request, 'vehiculo/tsa_update.html', {'form': form})
        else:
            form = ModificarTPPForm(instance=vehiculo)
            return render(request, 'vehiculo/tpp_update.html', {'form': form})


'''
DESINFECCIONES
'''


def get_quincena():
    return 'Primera' if timezone.now().day <= 15 else 'Segunda'


def get_vencimiento(fecha_realizacion):
    proximo_vencimiento = fecha_realizacion + relativedelta(months=1)
    if fecha_realizacion.day <= 15:
        return proximo_vencimiento.replace(day=15)
    else:
        return proximo_vencimiento.replace(day=monthrange(proximo_vencimiento.year, proximo_vencimiento.month)[1])


def get_estado(desinfecciones):
    estado = 'Al dia'
    if desinfecciones:
        if desinfecciones[0].proximo_vencimiento < timezone.now().date():
            estado = 'Atrasado'
        elif desinfecciones[0].proximo_vencimiento.month == timezone.now().month:
            estado = 'Quincena en curso'
    return estado


@login_required(login_url='login')
def lista_desinfecciones(request, pk_vehiculo):
    listado_desinfecciones = Desinfeccion.objects.filter(vehiculo__pk=pk_vehiculo).order_by('-fecha_realizacion')
    estado = get_estado(listado_desinfecciones)
    return render(request, 'desinfeccion/desinfeccion_list.html', {'listado': listado_desinfecciones,
                                                                   'estado': estado, 'pk_vehiculo': pk_vehiculo})


@login_required(login_url='login')
def nueva_desinfeccion(request, pk_vehiculo):
    listado_desinfecciones = Desinfeccion.objects.filter(vehiculo__pk=pk_vehiculo).order_by('-fecha_realizacion')
    estado = get_estado(listado_desinfecciones)
    vehiculo = Vehiculo.objects.get(pk=pk_vehiculo)
    if request.method == 'POST':
        form = DesinfeccionForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        if form.is_valid() & detalle_mov_form.is_valid():
            desinfeccion = form.save(commit=False)
            desinfeccion.vehiculo = vehiculo
            desinfeccion.quincena = 'Primera' if desinfeccion.fecha_realizacion.day <= 15 else 'Segunda'
            desinfeccion.proximo_vencimiento = get_vencimiento(desinfeccion.fecha_realizacion)
            desinfeccion.save()
            detalle_mov = detalle_mov_form.save(commit=False)
            importe = 0
            if vehiculo.tipo_vehiculo == 'TPP' and vehiculo.tipo_tpp == 'Colectivo':
                servicio = pd_m.Servicio.objects.get(nombre="Desinfeccion: Colectivo")
            else:
                servicio = pd_m.Servicio.objects.get(nombre="Desinfeccion: Taxi, Remisse, Escolar, TSA")
            if estado == 'Atrasado':
                importe = servicio.importe * 2
            detalle_mov.importe = importe
            detalle_mov.descripcion = str(servicio) + " | N° " + str(desinfeccion.id)
            detalle_mov.servicio = str(servicio)
            detalle_mov.save()
            log_crear(request.user.id, desinfeccion, 'Desinfeccion')
            return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=pk_vehiculo))
    else:
        form = DesinfeccionForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
    return render(request, 'desinfeccion/desinfeccion_form.html', {'estado': estado, 'vehiculo': vehiculo,
                                                                   'form': form, 'detalle_mov_form': detalle_mov_form})


@login_required(login_url='login')
def baja_desinfeccion(request, pk):
    desinfeccion = Desinfeccion.objects.get(pk=pk)
    log_eliminar(request.user.id, desinfeccion, 'Desinfeccion')
    desinfeccion.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificar_desinfeccion(request, pk_vehiculo, pk):
    desinfeccion = Desinfeccion.objects.get(pk=pk)
    if request.method == 'POST':
        form = DesinfeccionForm(request.POST, instance=desinfeccion)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Desinfeccion')
            return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=pk_vehiculo))
    else:
        form = DesinfeccionForm(instance=desinfeccion)
    return render(request, 'desinfeccion/desinfeccion_form.html', {'form': form, 'modificacion': True,
                                                                   'vehiculo': Vehiculo.objects.get(pk=pk_vehiculo)})


'''
CONTROL DE PLAGAS
'''


@login_required(login_url='login')
def lista_controles_plaga(request):
    return render(request, 'controlPlaga/control_plaga_list.html', {'listado': ControlDePlaga.objects.all()})


@login_required(login_url='login')
def alta_control_plaga(request):
    if request.method == 'POST':
        form = ControlDePlagaForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        pago_diferido_form = PagoDiferidoForm(request.POST)
        if form.is_valid():
            servicio = pd_m.Servicio.objects.get(nombre='Fumigacion, desinfeccion, desratizacion')
            if request.POST['optradio'] == 'normal':
                if detalle_mov_form.is_valid():
                    control_plaga = form.save()
                    detalle_mov = detalle_mov_form.save(commit=False)
                    detalle_mov.completar(servicio, control_plaga)
                    log_crear(request.user.id, control_plaga, 'Control de Plagas')
                    return redirect('controles_plagas:lista_controles_plagas')
            else:
                if pago_diferido_form.is_valid():
                    control_plaga = form.save()
                    control_plaga.pagado = False
                    control_plaga.save()
                    pago = pago_diferido_form.save(commit=False)
                    pago.detalles(servicio, control_plaga)
                    log_crear(request.user.id, control_plaga, 'Control de Plagas')
                    return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ControlDePlagaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        pago_diferido_form = PagoDiferidoForm()
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                                    'pago_diferido_form': pago_diferido_form})


class DetalleControlPlaga(LoginRequiredMixin, DetailView):
    model = ControlDePlaga
    template_name = 'controlPlaga/control_plaga_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def baja_control_plaga(request, pk):
    control_plaga = ControlDePlaga.objects.get(pk=pk)
    log_eliminar(request.user.id, control_plaga, 'Control de Plagas')
    control_plaga.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_control_plaga(request, pk):
    control_plaga = ControlDePlaga.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionControlDePlagaForm(request.POST, instance=control_plaga)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Control de Plagas')
            return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ModificacionControlDePlagaForm(instance=control_plaga)
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form, 'modificacion': True})


@login_required(login_url='login')
def pago_diferido(request, pk):
    control = ControlDePlaga.objects.get(pk=pk)
    pago = PagoDiferido.objects.get(control=control)
    if request.method == 'POST':
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        if detalle_mov_form.is_valid():
            detalle_mov = detalle_mov_form.save(commit=False)
            detalle_mov.importe = pago.monto
            detalle_mov.descripcion = 'Fumigacion, desinfeccion, desratizacion'
            detalle_mov.save()
            control.pagado = True
            control.save()
            log_crear(request.user.id, pago, 'Pago de Control de Plagas')
            return redirect('controles_plagas:lista_controles_plagas')
    else:
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
    return render(request, 'controlPlaga/pago_control_form.html', {'detalle_mov_form': detalle_mov_form})


@login_required(login_url='login')
def estadisticas_vehiculos(request):
    rango_form = dp_f.RangoFechaForm
    anio = timezone.now().year
    years = range(anio, anio - 5, -1)
    if request.method == 'POST':
        rango_form = dp_f.RangoFechaForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']
            anio_desde = fecha_desde.year
            anio_hasta = fecha_hasta.year
            years = range(anio_hasta, anio_desde - 1, -1)

    des_tr = {}  # desinfeccion taxi/remis
    des_escolares = {}
    des_tsa = {}
    des_colectivos = {}

    for year in years:

        # acumuladores
        tr = 0
        escolares = 0
        tsa = 0
        colectivos = 0

        desinfecciones_vehiculos = Desinfeccion.objects.filter(fecha_realizacion__year=year).values_list(
            "vehiculo__tipo_vehiculo", "vehiculo__tipo_tpp")

        for des in desinfecciones_vehiculos:
            if des[0] == 'TSA':
                tsa += 1
            elif des[1] == 'Colectivo':
                colectivos += 1
            elif des[1] == 'TR':
                tr += 1
            else:
                escolares += 1

        des_tsa[str(year)] = tsa
        des_tr[str(year)] = tr
        des_colectivos[str(year)] = colectivos
        des_escolares[str(year)] = escolares

    # desinfecciones vehiculos

    ord_des_tsa = collections.OrderedDict(sorted(des_tsa.items()))
    ord_des_tr = collections.OrderedDict(sorted(des_tr.items()))
    ord_des_colectivos = collections.OrderedDict(sorted(des_colectivos.items()))
    ord_des_escolares = collections.OrderedDict(sorted(des_escolares.items()))

    label_categoria_des = ord_des_tsa.keys()  # indistinto para los datos (tienen la misma clave)
    datos_des_tsa = ord_des_tsa.values()
    datos_des_tr = ord_des_tr.values()
    datos_des_colectivos = ord_des_colectivos.values()
    datos_des_escolares = ord_des_escolares.values()

    context = {
        'rango_form': rango_form,
        # mascotas
        'promedio_tsa': int(np.average(datos_des_tsa)),
        'promedio_tr': int(np.average(datos_des_tr)),
        'promedio_colectivos': int(np.average(datos_des_colectivos)),
        'promedio_escolares': int(np.average(datos_des_escolares)),
        # datos y etiquetas
        'lista_labels': json.dumps([label_categoria_des]),
        'lista_datos': json.dumps([{'TSA': datos_des_tsa, 'Taxis/Remiss': datos_des_tr,
                                    'Colectivos': datos_des_colectivos, 'Escolares': datos_des_escolares},
                                ])
    }

    return render(request, "estadistica/estadisticas_vehiculos.html", context)
