# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
import calendar
from dateutil.relativedelta import relativedelta
from personas import forms as f
from .forms import *
from .choices import *
from parte_diario_caja import forms as pd_f
from parte_diario_caja import models as pd_m
from parte_diario_caja import views as pd_v
from desarrollo_patagonia import forms as dp_f
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from desarrollo_patagonia.utils import *
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin
from django.utils import timezone
import collections
import json
import numpy as np
from weasyprint import HTML
from django.template.loader import get_template


def limpiar_periodos(cc):
    periodos = PeriodoCC.objects.filter(cc=cc)
    detalles = DetalleCC.objects.all().values_list('periodo', flat=True)
    for periodo in periodos:
        if periodo.pk not in detalles:
            periodo.delete()


def enlazar_detalles():
    detalles = DetalleCC.objects.filter(periodo__isnull=True)
    for detalle in detalles:
        try:
            periodo = PeriodoCC.objects.get(periodo__month=detalle.reinspeccion.fecha.month,
                                            periodo__year=detalle.reinspeccion.fecha.year,
                                            cc=CuentaCorriente.objects.get(abastecedor=detalle.reinspeccion.abastecedor))
        except:
            periodo = PeriodoCC.objects.create(periodo=detalle.reinspeccion.fecha, importe=detalle.reinspeccion.importe,
                                               total_kg=detalle.reinspeccion.total_kg,
                                               cc=CuentaCorriente.objects.get(
                                                   abastecedor=detalle.reinspeccion.abastecedor))
        periodo.save()
        detalle.periodo = periodo
        detalle.save()


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
    enlazar_detalles()
    return render(request, 'cuentaCorriente/cc_list.html', {'listado': CuentaCorriente.objects.all()})


@login_required(login_url='login')
def periodos_cc(request, pk):
    cc = CuentaCorriente.objects.get(pk=pk)
    limpiar_periodos(cc)
    return render(request, 'cuentaCorriente/cc_periodos.html', {'pk': pk, 'listado': PeriodoCC.objects.filter(cc=cc)})


@login_required(login_url='login')
def detalle_periodo(request, pk):
    periodo = PeriodoCC.objects.get(pk=pk)
    return render(request, 'cuentaCorriente/periodo_detail.html', {'listado': DetalleCC.objects.filter(periodo=periodo),
                                                                   'periodo': periodo})


def agrupar_reinspecciones(periodo):
    reinspecciones = []
    detalles = DetalleCC.objects.filter(periodo=periodo).order_by('reinspeccion__fecha')
    for detalle in detalles:
        productos = ReinspeccionProducto.objects.filter(reinspeccion=detalle.reinspeccion)
        reinspecciones.append({'reinspeccion': detalle.reinspeccion, 'productos': productos})
    return reinspecciones


@login_required(login_url='login')
def certificado_deuda(request, pk):
    periodo = PeriodoCC.objects.get(pk=pk)
    reinspecciones = agrupar_reinspecciones(periodo)
    if request.method == 'POST':
        periodo.fecha_certificado = now()
        periodo.save()
        return HttpResponseRedirect(reverse('cuentas_corrientes:periodos_cc', args=[periodo.cc.pk]))
    return render(request, 'cuentaCorriente/certificado_deuda.html', {'periodo': periodo,
                                                                      'reinspecciones': reinspecciones})


@login_required(login_url='login')
def pdf_certificado(request, pk):
    template = get_template('cuentaCorriente/certificado_pdf.html')
    periodo = PeriodoCC.objects.get(pk=pk)
    reinspecciones = agrupar_reinspecciones(periodo)
    context = {'periodo': periodo, 'reinspecciones': reinspecciones,
               'title': 'Certificado de deuda - ' + str(periodo.cc.abastecedor.responsable.nombre)
                        + ' / Periodo: ' + str(periodo.periodo.month) + '-' + str(periodo.periodo.year)}
    rendered = template.render(context)
    pdf_file = HTML(string=rendered, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' + str("Certificado_deuda_"
                                                        + str(periodo.cc.abastecedor.responsable.nombre))
    return response


@login_required(login_url='login')
def abonar_certificado(request, pk):
    periodo = PeriodoCC.objects.get(pk=pk)
    delta = np.busday_count(periodo.fecha_certificado, timezone.now().date(), holidays=['Y-04-29'])
    delta += 1
    importe = periodo.importe
    if delta > 5:
        importe += (importe * 0.008 * (delta - 5))
    if request.method == 'POST':
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        periodo.pagado = True
        servicio = "Cancelacion de deuda en Cuenta Corriente"
        if request.POST['optradio'] == 'previa':
            periodo.save()
            nro_ingreso = int(request.POST['selected_mov'])
            movimiento = pd_m.MovimientoDiario.objects.get(nro_ingreso=nro_ingreso)
            detalle_mov = pd_m.DetalleMovimiento.objects.create(movimiento=movimiento, importe=0)
            detalle_mov.completar_monto(importe, servicio, periodo.cc)
            log_crear(request.user.id, periodo.cc, servicio)
            return HttpResponseRedirect(reverse('cuentas_corrientes:periodos_cc', args=[periodo.cc.pk]))
        else:
            if mov_form.is_valid():
                periodo.save()
                mov = mov_form.save()
                detalle_mov = pd_m.DetalleMovimiento(movimiento=mov)
                detalle_mov.completar_monto(importe, servicio, periodo.cc)
                log_crear(request.user.id, periodo.cc, servicio)
                return HttpResponseRedirect(reverse('cuentas_corrientes:periodos_cc', args=[periodo.cc.pk]))
    else:
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'cuentaCorriente/abonar_certificado.html', {'periodo': periodo, 'atraso': delta - 5,
                                                                       'importe': importe, 'mov_form': mov_form})


'''
REINSPECCIONES
'''


@login_required(login_url='login')
def lista_reinspeccion(request):
    return render(request, 'reinspeccion/reinspeccion_list.html')


def datatable_preloader(request):

    filtro = request.GET.get('filtro')

    data = []
    resul = []

    if filtro:
        resul  =  Reinspeccion.objects.filter(abastecedor__responsable__nombre__icontains=filtro)

    for f in resul:
        f.fecha = f.fecha.strftime('%d/%m/%Y')
        data.append(f.to_json())

    response = {'listado': data, 'user_staff':request.user.is_staff}
    return JsonResponse(response)



@login_required(login_url='login')
def alta_reinspeccion(request):
    if request.method == 'POST':
        form = ReinspeccionForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        servicio = 'Reinspeccion Veterinaria'
        if form.is_valid():
            reinspeccion = form.save(commit=False)
            reinspeccion.detalles = False
            reinspeccion.save()
            form.save_m2m()
            if request.POST['optradio'] == 'previa':
                nro_ingreso = int(request.POST['selected_mov'])
                movimiento = pd_m.MovimientoDiario.objects.get(nro_ingreso=nro_ingreso)
                detalle_mov = pd_m.DetalleMovimiento.objects.create(movimiento=movimiento, importe=0)
                detalle_mov.completar_monto(reinspeccion.importe, servicio, reinspeccion)
                log_crear(request.user.id, reinspeccion, servicio)
                return redirect('reinspecciones:lista_reinspecciones')
            else:
                if mov_form.is_valid():
                    mov = mov_form.save()
                    detalle_mov = pd_m.DetalleMovimiento(movimiento=mov)
                    detalle_mov.completar_monto(reinspeccion.importe, servicio, reinspeccion)
                    log_crear(request.user.id, reinspeccion, servicio)
                    return redirect('reinspecciones:lista_reinspecciones')
    else:
        form = ReinspeccionForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'reinspeccion/reinspeccion_form.html', {'form': form, 'mov_form': mov_form})


@login_required(login_url='login')
def baja_reinspeccion(request, pk):
    reinspeccion = Reinspeccion.objects.get(pk=pk)
    log_eliminar(request.user.id, reinspeccion, 'Reinspeccion Veterinaria')
    reinspeccion.delete()
    return HttpResponse()


def calculo_importe(total_kg):
    precios = ReinspeccionPrecios.objects.get()
    monto = precios.precio_min
    if total_kg > precios.kg_min:
        monto = total_kg * precios.precio_kg
    return monto


@login_required(login_url='login')
def calculo_importe_json(request, kg):
    total_kg = int(kg)
    precios = ReinspeccionPrecios.objects.get()
    monto = precios.precio_min
    if total_kg > precios.kg_min:
        monto = total_kg * precios.precio_kg
    return JsonResponse({'importe': monto})


@login_required(login_url='login')
def calculo_kg_importe(request):
    total_kg = sum(item['kilo_producto'] for item in request.session['productos'])
    precios = ReinspeccionPrecios.objects.get()
    monto = precios.precio_min
    if total_kg > precios.kg_min:
        monto = total_kg * precios.precio_kg
    return JsonResponse({'total_kg': total_kg, 'importe': monto})


@login_required(login_url='login')
def carga_productos(request, reinspeccion_pk):
    producto_form = ReinspeccionProductoForm
    mensaje = ''
    productos = []
    total_kg = 0
    if request.method == 'POST':
        productos = request.session['productos']
        total_kg = sum(item['kilo_producto'] for item in productos)
        reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
        if 'productos' in request.session:
            productos = request.session['productos']
        if total_kg != reinspeccion.total_kg:
            mensaje = 'La cantidad ingresada no coincide con el peso registrado. Por favor revise el detalle.'
        else:
            for producto in request.session['productos']:
                prod = Producto.objects.get(nombre=producto['producto']['nombre'])
                item = ReinspeccionProducto(producto=prod, kilo_producto=producto['kilo_producto'],
                                            reinspeccion=reinspeccion)
                item.save()
            reinspeccion.detalles = True
            reinspeccion.save()
            log_modificar(request.user.id, reinspeccion, 'Reinspeccion Veterinaria')
            return redirect('reinspecciones:lista_reinspecciones')
    else:
        if 'productos' in request.session:
            del request.session['productos']
        request.session['productos'] = []
    return render(request, 'reinspeccion/carga_productos.html',
                  {'producto_form': producto_form, 'mensaje': mensaje, 'productos': productos, 'total_kg': total_kg,
                   'reinspeccion': Reinspeccion.objects.get(pk=reinspeccion_pk)})


@login_required(login_url='login')
def alta_reinspeccion_cc(request):
    producto_form = ReinspeccionProductoForm
    productos = []
    if request.method == 'POST':
        form = ReinspeccionCCForm(request.POST)
        if 'productos' in request.session:
            productos = request.session['productos']
        if form.is_valid():
            reinspeccion = form.save(commit=False)
            reinspeccion.detalles = True
            reinspeccion.save()
            form.save_m2m()
            alta_productos(request, reinspeccion)
            detalle = DetalleCC(reinspeccion=reinspeccion)
            detalle.save()
            log_crear(request.user.id, reinspeccion, 'Reinspeccion Veterinaria')
            if '_fin' in request.POST:
                return redirect('reinspecciones:lista_reinspecciones')
            elif '_new' in request.POST:
                return redirect('reinspecciones:nueva_reinspeccion_cc')
    else:
        if 'productos' in request.session:
            del request.session['productos']
        request.session['productos'] = []
        form = ReinspeccionCCForm
    return render(request, 'reinspeccion/reinspeccion_cc_form.html', {'form': form, 'producto_form': producto_form,
                                                                      'productos': productos})


def existe_producto(request, producto):
    for item in request.session['productos']:
        if item['producto']['nombre'] == producto.producto.nombre:
            return True
    return False


@login_required(login_url='login')
def modificar_reinspeccion(request, pk, periodo_pk):
    reinspeccion = Reinspeccion.objects.get(pk=pk)
    if int(periodo_pk):
        periodo = PeriodoCC.objects.get(pk=periodo_pk)
        url_return = 'cuentas_corrientes:detalle_periodo'
        id_return = periodo_pk
    else:
        periodo = None
        url_return = 'reinspecciones:lista_reinspecciones'
        id_return = ""
    if request.method == 'POST':
        form = ModificarReinspeccionForm(request.POST, instance=reinspeccion)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Reinspeccion Veterinaria')
            if int(periodo_pk):
                return HttpResponseRedirect(reverse(url_return, args=[periodo_pk]))
            else:
                return redirect('reinspecciones:lista_reinspecciones')
    else:
        form = ModificarReinspeccionForm(instance=reinspeccion)
    return render(request, 'reinspeccion/reinspeccion_modificar.html', {'form': form, 'url_return': url_return,
                                                                        'id_return': id_return, 'periodo': periodo})


@login_required(login_url='login')
def agregar_producto_reinspeccion(request, reinspeccion_pk, periodo_pk):
    reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
    productos = ReinspeccionProducto.objects.filter(reinspeccion=reinspeccion).values_list('producto__nombre',
                                                                                           flat=True)
    msg = ""
    if request.method == 'POST':
        form = ReinspeccionProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            if producto.producto.nombre not in productos:
                producto.reinspeccion = reinspeccion
                producto.save()
                reinspeccion.total_kg += producto.kilo_producto
                reinspeccion.importe = calculo_importe(reinspeccion.total_kg)
                if reinspeccion.turno == 'Feriado':
                    reinspeccion.importe *= 2
                reinspeccion.save()
                log_modificar(request.user.id, reinspeccion, 'Reinspeccion Veterinaria')
                return HttpResponseRedirect(reverse('reinspecciones:lista_productos',
                                                    args=[reinspeccion_pk, periodo_pk]))
            else:
                msg = "Este producto ya se encuentra cargado"
    else:
        form = ReinspeccionProductoForm
    return render(request, 'reinspeccion/nuevo_producto_form.html', {'form': form, 'reinspeccion_pk': reinspeccion_pk,
                                                                     'periodo_pk': periodo_pk, 'msg': msg})


@login_required(login_url='login')
def agregar_producto(request):
    form = ReinspeccionProductoForm(request.POST)
    success = True
    total_kg = 0
    if form.is_valid():
        producto = form.save(commit=False)
        if existe_producto(request, producto):
            success = False
        else:
            request.session['productos'].append(producto.to_json())
            request.session.modified = True
            total_kg = sum(item['kilo_producto'] for item in request.session['productos'])

    return JsonResponse({'success': success, 'productos': request.session['productos'], 'total_kg': total_kg})


@login_required(login_url='login')
def eliminar_producto(request, nombre):
    productos = request.session['productos']
    productos[:] = [p for p in productos if p['producto']['nombre'] != nombre]
    request.session['productos'] = productos
    total_kg = sum(item['kilo_producto'] for item in request.session['productos'])
    return JsonResponse({'productos': request.session['productos'], 'total_kg': total_kg})


@login_required(login_url='login')
def modificar_producto(request, nombre, kg):
    productos = request.session['productos']
    for item in productos:
        if item['producto']['nombre'] == nombre:
            item['kilo_producto'] = int(kg)
    request.session['productos'] = productos
    total_kg = sum(item['kilo_producto'] for item in request.session['productos'])
    return JsonResponse({'productos': request.session['productos'], 'total_kg': total_kg})


@login_required(login_url='login')
def modificar_producto_reinspeccion(request, pk, nombre, kg):
    reinspeccion = Reinspeccion.objects.get(pk=pk)
    producto = ReinspeccionProducto.objects.get(reinspeccion=reinspeccion, producto__nombre=nombre)
    diferencia = producto.kilo_producto - float(kg)
    producto.kilo_producto = kg
    producto.save()
    reinspeccion.total_kg -= diferencia
    reinspeccion.importe = calculo_importe(reinspeccion.total_kg)
    reinspeccion.save()
    return HttpResponse()


def alta_productos(request, reinspeccion):
    for producto in request.session['productos']:
        prod = Producto.objects.get(nombre=producto['producto']['nombre'])
        item = ReinspeccionProducto(producto=prod, kilo_producto=producto['kilo_producto'], reinspeccion=reinspeccion)
        item.save()
    reinspeccion.save()
    return HttpResponse()


@login_required(login_url='login')
def lista_productos(request, reinspeccion_pk, periodo_pk):
    reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
    if int(periodo_pk):
        periodo = PeriodoCC.objects.get(pk=periodo_pk)
        url_return = 'cuentas_corrientes:detalle_periodo'
        id_return = periodo_pk
    else:
        periodo = None
        url_return = 'reinspecciones:lista_reinspecciones'
        id_return = ""
    return render(request, 'reinspeccion/producto_list.html',
                  {'reinspeccion': reinspeccion, 'url_return': url_return, 'id_return': id_return,
                   'listado': ReinspeccionProducto.objects.filter(reinspeccion=reinspeccion), 'periodo': periodo})


@login_required(login_url='login')
def borrar_producto(request, pk):
    producto = ReinspeccionProducto.objects.get(pk=pk)
    log_eliminar(request.user.id, producto, 'Producto de reinspección')
    producto.delete()
    return HttpResponse()


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


class AltaMarca(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = MarcaVehiculo
    form_class = MarcaVehiculoForm
    template_name = "vehiculo/marca_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaModelo(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = ModeloVehiculo
    form_class = ModeloVehiculoForm
    template_name = "vehiculo/modelo_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def alta_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            if vehiculo.tipo_vehiculo == 'TSA':
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
        form = ModificarTSAForm(request.POST, instance=vehiculo) if vehiculo.tipo_vehiculo == 'TSA' \
            else ModificarTPPForm(request.POST, instance=vehiculo)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            if vehiculo.tipo_vehiculo == 'TSA':
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


@login_required(login_url='login')
def pdf_desinfecciones(request, nro):
    template = get_template('vehiculo/pdf_desinfecciones.html')
    vehiculo = Vehiculo.objects.get(nro=nro)
    context = {'vehiculo': vehiculo, 'title': 'Vehiculo N°'}
    rendered = template.render(context)
    pdf_file = HTML(string=rendered, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' + str("Vehiculo_N°_" + str(nro))
    return response


@login_required(login_url='login')
def pdf_vehiculo(request, nro):
    template = get_template('vehiculo/pdf_vehiculo.html')
    vehiculo = Vehiculo.objects.get(nro=nro)
    context = {'vehiculo': vehiculo, 'title': 'Vehiculo N°'}
    rendered = template.render(context)
    pdf_file = HTML(string=rendered, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=' + str("Vehiculo_N°_" + str(nro))
    return response


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
        return proximo_vencimiento.replace(day=calendar.monthrange(proximo_vencimiento.year,
                                                                   proximo_vencimiento.month)[1])


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
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if form.is_valid():
            desinfeccion = form.save(commit=False)
            desinfeccion.vehiculo = vehiculo
            desinfeccion.quincena = 'Primera' if desinfeccion.fecha_realizacion.day <= 15 else 'Segunda'
            desinfeccion.proximo_vencimiento = get_vencimiento(desinfeccion.fecha_realizacion)
            desinfeccion.save()
            if vehiculo.tipo_vehiculo == 'TPP' and vehiculo.tipo_tpp == 'Colectivo':
                servicio = pd_m.Servicio.objects.get(nombre="Desinfeccion: Colectivo")
            else:
                servicio = pd_m.Servicio.objects.get(nombre="Desinfeccion: Taxi, Remisse, Escolar, TSA")
            importe = servicio.importe * 2 if estado == 'Atrasado' else servicio.importe
            if request.POST['optradio'] == 'previa':
                nro_ingreso = int(request.POST['selected_mov'])
                movimiento = pd_m.MovimientoDiario.objects.get(nro_ingreso=nro_ingreso)
                detalle_mov = pd_m.DetalleMovimiento.objects.create(movimiento=movimiento, importe=0)
                detalle_mov.importe = importe
                detalle_mov.descripcion = str(servicio) + " | N° " + str(desinfeccion.id)
                detalle_mov.servicio = str(servicio)
                detalle_mov.save()
                log_crear(request.user.id, desinfeccion, 'Desinfeccion')
                return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=[pk_vehiculo]))
            else:
                if mov_form.is_valid():
                    mov = mov_form.save()
                    detalle_mov = pd_m.DetalleMovimiento(movimiento=mov)
                    detalle_mov.importe = importe
                    detalle_mov.descripcion = str(servicio) + " | N° " + str(desinfeccion.id)
                    detalle_mov.servicio = str(servicio)
                    detalle_mov.save()
                    log_crear(request.user.id, desinfeccion, 'Desinfeccion')
                    return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=[pk_vehiculo]))

    else:
        form = DesinfeccionForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'desinfeccion/desinfeccion_form.html', {'estado': estado, 'vehiculo': vehiculo,
                                                                   'form': form, 'mov_form': mov_form})


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
            return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=[pk_vehiculo]))
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
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        pago_diferido_form = PagoDiferidoForm(request.POST)
        if form.is_valid():
            servicio = "Fumigacion, desinfeccion, desratizacion"
            if request.POST['radio_tipo_pago'] == 'normal':
                if request.POST['optradio'] == 'previa':
                    control_plaga = form.save()
                    VisitaControl(fecha=form.cleaned_data['fecha_prox_visita'], control=control_plaga).save()
                    nro_ingreso = int(request.POST['selected_mov'])
                    movimiento = pd_m.MovimientoDiario.objects.get(nro_ingreso=nro_ingreso)
                    pd_v.movimiento_previo(request, movimiento, servicio, control_plaga, 'Control de plagas')
                    return redirect('controles_plagas:lista_controles_plagas')
                else:
                    if mov_form.is_valid():
                        control_plaga = form.save()
                        VisitaControl(fecha=form.cleaned_data['fecha_prox_visita'], control=control_plaga).save()
                        pd_v.nuevo_movimiento(request, mov_form, servicio, control_plaga, 'Control de plagas')
                        return redirect('controles_plagas:lista_controles_plagas')
            else:
                if pago_diferido_form.is_valid():
                    control_plaga = form.save(commit=False)
                    control_plaga.pagado = False
                    control_plaga.save()
                    VisitaControl(fecha=form.cleaned_data['fecha_prox_visita'], control=control_plaga).save()
                    pago = pago_diferido_form.save(commit=False)
                    pago.detalles(servicio, control_plaga)
                    log_crear(request.user.id, control_plaga, 'Control de Plagas')
                    return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ControlDePlagaForm
        mov_form = pd_f.MovimientoDiarioForm
        pago_diferido_form = PagoDiferidoForm
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form, 'mov_form': mov_form,
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
            log_modificar(request.user.id, form.save(), 'Control de Plagas')
            return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ModificacionControlDePlagaForm(instance=control_plaga)
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form, 'modificacion': True})


@login_required(login_url='login')
def pago_diferido(request, pk):
    control = ControlDePlaga.objects.get(pk=pk)
    pago = PagoDiferido.objects.get(control=control)
    if request.method == 'POST':
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if request.POST['optradio'] == 'previa':
            nro_ingreso = int(request.POST['selected_mov'])
            movimiento = pd_m.MovimientoDiario.objects.get(nro_ingreso=nro_ingreso)
            detalle_mov = pd_m.DetalleMovimiento.objects.create(movimiento=movimiento, importe=0)
            detalle_mov.descripcion = 'Fumigacion, desinfeccion, desratizacion' + " | N° " + str(control.id)
            detalle_mov.importe = pago.monto
            detalle_mov.servicio = 'Fumigacion, desinfeccion, desratizacion'
            detalle_mov.save()
            control.pagado = True
            control.save()
            log_crear(request.user.id, pago, 'Pago de Control de Plagas')
            return redirect('controles_plagas:lista_controles_plagas')
        else:
            if mov_form.is_valid():
                mov = mov_form.save()
                detalle_mov = pd_m.DetalleMovimiento(movimiento=mov)
                detalle_mov.descripcion = 'Fumigacion, desinfeccion, desratizacion' + " | N° " + str(control.id)
                detalle_mov.importe = pago.monto
                detalle_mov.servicio = 'Fumigacion, desinfeccion, desratizacion'
                detalle_mov.save()
                control.pagado = True
                control.save()
                log_crear(request.user.id, pago, 'Pago de Control de Plagas')
                return redirect('controles_plagas:lista_controles_plagas')
    else:
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'controlPlaga/pago_control_form.html', {'mov_form': mov_form})


def visitas_control_plaga(request, pk):
    control = ControlDePlaga.objects.get(pk=pk)
    return render(request, 'controlPlaga/control_plaga_visitas.html',
                  {'listado': VisitaControl.objects.filter(control=control)})


def mod_visita_control_plaga(request, pk):
    visita = VisitaControl.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionVisitaControlForm(request.POST, instance=visita)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Visita de Control de Plagas')
            return HttpResponseRedirect(reverse('controles_plagas:visitas_control_plaga', args=[visita.control.pk]))
    else:
        form = ModificacionVisitaControlForm(instance=visita)
    return render(request, 'controlPlaga/control_plaga_visita_form.html', {'form': form, 'visita': visita})


def reg_visita_control_plaga(request, pk):
    visita = VisitaControl.objects.get(pk=pk)
    if request.method == 'POST':
        form = VisitaControlForm(request.POST, instance=visita)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.realizada = True
            visita.save()
            if form.cleaned_data['fecha_prox_visita']:
                VisitaControl(fecha=form.cleaned_data['fecha_prox_visita'], control=visita.control).save()
            log_modificar(request.user.id, visita, 'Visita de Control de Plagas')
            return HttpResponseRedirect(reverse('controles_plagas:visitas_control_plaga',
                                                args=[visita.control.pk]))
    else:
        form = VisitaControlForm(instance=visita)
    return render(request, 'controlPlaga/control_plaga_visita_form.html', {'form': form, 'visita': visita})


'''
ESTADISTICAS
'''


@login_required(login_url='login')
def estadisticas_td(request):
    rango_form = dp_f.RangoAnioForm
    years = [timezone.now().year]
    if request.method == 'POST':
        rango_form = dp_f.RangoAnioForm(request.POST)
        if rango_form.is_valid():
            years = range(int(rango_form.cleaned_data['anio_hasta']),
                          int(rango_form.cleaned_data['anio_desde']) - 1, -1)

    des_tr, des_escolares, des_tsa, des_colectivos = {}, {}, {}, {}

    for year in years:
        tr, escolares, tsa, colectivos, = 0, 0, 0, 0

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

    # DESINFECCION DE VEHICULOS
    ord_des_tsa = collections.OrderedDict(sorted(des_tsa.items()))
    ord_des_tr = collections.OrderedDict(sorted(des_tr.items()))
    ord_des_colectivos = collections.OrderedDict(sorted(des_colectivos.items()))
    ord_des_escolares = collections.OrderedDict(sorted(des_escolares.items()))

    label_categoria_des = ord_des_tsa.keys()  # indistinto para los datos (tienen la misma clave)
    datos_des_tsa = ord_des_tsa.values()
    datos_des_tr = ord_des_tr.values()
    datos_des_colectivos = ord_des_colectivos.values()
    datos_des_escolares = ord_des_escolares.values()

    # CONTROL DE PLAGAS
    ctr_anual = to_counter(ControlDePlaga, {'fecha__year__lte': years[0], 'fecha__year__gte': years[-1]},
                           ['tipo_plaga'])
    total_general = sum(ctr_anual.values())
    dic = {}
    for k, v in ctr_anual.items():
        dic[k] = (v, float("{0:.2f}".format(v * 100 / total_general)))

    context = {
        'rango_form': rango_form,
        'ctr_anual': dic,
        # datos y etiquetas
        'lista_labels': json.dumps([label_categoria_des, ctr_anual.keys()]),
        'lista_datos': json.dumps([{'TSA': datos_des_tsa, 'Taxis/Remiss': datos_des_tr,
                                    'Colectivos': datos_des_colectivos, 'Escolares': datos_des_escolares},
                                   {'Controles': ctr_anual.values()}
                                   ])
    }
    return render(request, "estadistica/estadisticas_TD.html", context)


@login_required(login_url='login')
def estadisticas_reinspeccion(request):
    rango_form = dp_f.RangoAnioForm
    years = [timezone.now().year]
    if request.method == 'POST':
        rango_form = dp_f.RangoAnioForm(request.POST)
        if rango_form.is_valid():
            years = range(int(rango_form.cleaned_data['anio_hasta']),
                          int(rango_form.cleaned_data['anio_desde']) - 1, -1)

    reinspecciones = ReinspeccionProducto.objects.filter(reinspeccion__fecha__year__lte=years[0],
                                                         reinspeccion__fecha__year__gte=years[-1]).values_list(
        'producto__nombre', 'kilo_producto')
    dict_reinspeccion_prod = {}
    for prod, valor in reinspecciones:
        total = dict_reinspeccion_prod.get(prod, 0) + valor
        dict_reinspeccion_prod[prod] = total

    total_general = sum(dict_reinspeccion_prod.values())
    ord_dict_reinspeccion_prod = collections.OrderedDict(
        sorted(dict_reinspeccion_prod.iteritems(), key=lambda (k, v): (k, v)))  # Ordena los servicios por importe

    label_reinspeccion = ord_dict_reinspeccion_prod.keys()  # indistinto para los datos (tienen la misma clave)
    datos_reinspecciones = ord_dict_reinspeccion_prod.values()

    for k, v in ord_dict_reinspeccion_prod.items():
        ord_dict_reinspeccion_prod[k] = (v, float("{0:.2f}".format(v * 100 / total_general)))

    context = {
        'rango_form': rango_form,
        'dict': ord_dict_reinspeccion_prod,
        'total_general': total_general,
        # datos y etiquetas
        'lista_labels': json.dumps([label_reinspeccion]),
        'lista_datos': json.dumps([{'Productos': datos_reinspecciones}])
    }
    return render(request, "estadistica/estadisticas_reinspeccion.html", context)


@login_required(login_url='login')
def estadisticas_td(request):
    rango_form = dp_f.RangoAnioForm
    years = [timezone.now().year]
    if request.method == 'POST':
        rango_form = dp_f.RangoAnioForm(request.POST)
        if rango_form.is_valid():
            years = range(int(rango_form.cleaned_data['anio_hasta']),
                          int(rango_form.cleaned_data['anio_desde']) - 1, -1)

    des_tr, des_escolares, des_tsa, des_colectivos = {}, {}, {}, {}

    for year in years:
        tr, escolares, tsa, colectivos = 0, 0, 0, 0

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

    # DESINFECCION DE VEHICULOS
    ord_des_tsa = collections.OrderedDict(sorted(des_tsa.items()))
    ord_des_tr = collections.OrderedDict(sorted(des_tr.items()))
    ord_des_colectivos = collections.OrderedDict(sorted(des_colectivos.items()))
    ord_des_escolares = collections.OrderedDict(sorted(des_escolares.items()))

    label_categoria_des = ord_des_tsa.keys()  # indistinto para los datos (tienen la misma clave)
    datos_des_tsa = ord_des_tsa.values()
    datos_des_tr = ord_des_tr.values()
    datos_des_colectivos = ord_des_colectivos.values()
    datos_des_escolares = ord_des_escolares.values()

    # CONTROL DE PLAGAS
    ctr_anual = to_counter(ControlDePlaga, {'fecha__year__lte': years[0], 'fecha__year__gte': years[-1]},
                           ['tipo_plaga'])
    total_general = sum(ctr_anual.values())
    dic = {}
    for k, v in ctr_anual.items():
        dic[k] = (v, float("{0:.2f}".format(v * 100 / total_general)))

    context = {
        'rango_form': rango_form,
        'ctr_anual': dic,
        # datos y etiquetas
        'lista_labels': json.dumps([label_categoria_des, ctr_anual.keys()]),
        'lista_datos': json.dumps([{'TSA': datos_des_tsa, 'Taxis/Remiss': datos_des_tr,
                                    'Colectivos': datos_des_colectivos, 'Escolares': datos_des_escolares},
                                   {'Controles': ctr_anual.values()}
                                   ])
    }
    return render(request, "estadistica/estadisticas_TD.html", context)


@login_required(login_url='login')
def estadisticas_reinspeccion(request):
    rango_form = dp_f.RangoFechaForm
    fecha_desde = timezone.now() - relativedelta(years=1)
    fecha_hasta = timezone.now()
    if request.method == 'POST':
        rango_form = dp_f.RangoFechaForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']

    reinspecciones_data = ReinspeccionProducto.objects.filter(reinspeccion__fecha__gte=fecha_desde,
                                                              reinspeccion__fecha__lte=fecha_hasta,
                                                              reinspeccion__detalles=True) \
        .values_list('reinspeccion__origen__nombre', 'producto__nombre', 'kilo_producto')

    reinspecciones = Reinspeccion.objects.filter(fecha__gte=fecha_desde, fecha__lte=fecha_hasta, detalles=True)

    dict_reinspeccion_prod, dict_reinspeccion_orig_r, dict_reinspeccion_orig_kg = {}, {}, {}
    dict_reinspeccion_gan = {'Bovinos': {}, 'Bovinos sin hueso': {}, 'Porcinos': {}, 'Ovinos': {}}
    dict_reinspeccion_gan_orig = collections.defaultdict(dict)

    for orig, prod, cant_kg in reinspecciones_data:
        total_kg_prod = dict_reinspeccion_prod.get(prod, 0) + cant_kg
        total_kg_orig = dict_reinspeccion_orig_kg.get(orig, 0) + cant_kg
        dict_reinspeccion_prod[prod] = total_kg_prod
        dict_reinspeccion_orig_kg[orig] = total_kg_orig

        if prod.lower() in ['bovinos', 'bovinos sin hueso', 'porcinos', 'ovinos']:
            if prod.lower() == 'bovinos sin hueso':
                prod = 'Bovinos sin hueso'
            if orig not in dict_reinspeccion_gan['Bovinos']:
                dict_reinspeccion_gan['Bovinos'][orig] = 0
                dict_reinspeccion_gan['Bovinos sin hueso'][orig] = 0
                dict_reinspeccion_gan['Porcinos'][orig] = 0
                dict_reinspeccion_gan['Ovinos'][orig] = 0
            dict_reinspeccion_gan[prod][orig] += cant_kg

    for reinspeccion in reinspecciones:
        total_cant = dict_reinspeccion_orig_r.get(reinspeccion.origen.nombre, 0) + 1
        dict_reinspeccion_orig_r[reinspeccion.origen.nombre] = total_cant

    total_general_prod = sum(dict_reinspeccion_prod.values())
    ord_dict_reinspeccion_prod = collections.OrderedDict(
        sorted(dict_reinspeccion_prod.iteritems(), key=lambda (k, v): (k, v)))

    total_general_orig_r = sum(dict_reinspeccion_orig_r.values())
    total_general_orig_kg = sum(dict_reinspeccion_orig_kg.values())
    ord_dict_reinspeccion_orig = collections.OrderedDict(
        sorted(dict_reinspeccion_orig_r.iteritems(), key=lambda (k, v): (k, v)))
    ord_dict_reinspeccion_orig_kg = collections.OrderedDict(
        sorted(dict_reinspeccion_orig_kg.iteritems(), key=lambda (k, v): (k, v)))

    label_reinspeccion = ord_dict_reinspeccion_prod.keys()
    datos_reinspecciones = ord_dict_reinspeccion_prod.values()
    label_origen_cant = ord_dict_reinspeccion_orig.keys()
    datos_origen_cant = ord_dict_reinspeccion_orig.values()
    label_origen_kg = ord_dict_reinspeccion_orig_kg.keys()
    datos_origen_kg = ord_dict_reinspeccion_orig_kg.values()
    label_gan = dict_reinspeccion_gan['Bovinos'].keys()

    for k, v in ord_dict_reinspeccion_prod.items():
        ord_dict_reinspeccion_prod[k] = (v, float("{0:.2f}".format(v * 100 / total_general_prod)))

    for k, v in ord_dict_reinspeccion_orig.items():
        cant_kg = dict_reinspeccion_orig_kg.get(k, 0)
        ord_dict_reinspeccion_orig[k] = (v, float("{0:.2f}".format(v * 100 / total_general_orig_r)), cant_kg,
                                         float("{0:.2f}".format(cant_kg * 100 / total_general_orig_kg)))

    orden = ['Bovinos', 'Bovinos sin hueso', 'Porcinos', 'Ovinos', 'total_kg']
    for orig in label_gan:
        dict_reinspeccion_gan_orig[orig]['Bovinos'] = dict_reinspeccion_gan['Bovinos'][orig]
        dict_reinspeccion_gan_orig[orig]['Bovinos sin hueso'] = dict_reinspeccion_gan['Bovinos sin hueso'][orig]
        dict_reinspeccion_gan_orig[orig]['Porcinos'] = dict_reinspeccion_gan['Porcinos'][orig]
        dict_reinspeccion_gan_orig[orig]['Ovinos'] = dict_reinspeccion_gan['Ovinos'][orig]
        dict_reinspeccion_gan_orig[orig]['total_kg'] = sum(dict_reinspeccion_gan_orig[orig].values())
        dict_reinspeccion_gan_orig[orig] = collections.OrderedDict(sorted(dict_reinspeccion_gan_orig[orig].items(),
                                                                          key=lambda i: orden.index(i[0])))

    total_general_gan = sum(origen['total_kg'] for origen in dict_reinspeccion_gan_orig.values())

    context = {
        'rango_form': rango_form,
        'dict_prod': ord_dict_reinspeccion_prod,
        'dict_orig': ord_dict_reinspeccion_orig,
        'dict_gan': collections.OrderedDict(dict_reinspeccion_gan_orig),
        'total_general_prod': total_general_prod,
        'total_general_orig_r': total_general_orig_r,
        'total_general_orig_kg': total_general_orig_kg,
        'total_bovinos': sum(origen['Bovinos'] for origen in dict_reinspeccion_gan_orig.values()),
        'total_bovinos_sh': sum(origen['Bovinos sin hueso'] for origen in dict_reinspeccion_gan_orig.values()),
        'total_porcinos': sum(origen['Porcinos'] for origen in dict_reinspeccion_gan_orig.values()),
        'total_ovinos': sum(origen['Ovinos'] for origen in dict_reinspeccion_gan_orig.values()),
        'total_general_gan': total_general_gan,
        # datos y etiquetas
        'lista_labels': json.dumps([label_reinspeccion, label_origen_cant, label_origen_kg, label_gan]),
        'lista_datos': json.dumps([{'Productos': datos_reinspecciones},
                                   {'Origenes por cantidad': datos_origen_cant},
                                   {'Origenes por kg': datos_origen_kg},
                                   {'Bovinos': dict_reinspeccion_gan['Bovinos'].values(),
                                    'Bovinos sin hueso': dict_reinspeccion_gan['Bovinos sin hueso'].values(),
                                    'Porcinos': dict_reinspeccion_gan['Porcinos'].values(),
                                    'Ovinos': dict_reinspeccion_gan['Ovinos'].values()}])
    }
    return render(request, "estadistica/estadisticas_reinspeccion.html", context)
