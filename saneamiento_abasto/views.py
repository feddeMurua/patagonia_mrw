# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
import calendar
import locale
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
from easy_pdf.views import PDFTemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin
from django.utils import timezone
import collections
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
def detalle_cc(request, pk):
    cuenta = CuentaCorriente.objects.get(pk=pk)
    if request.method == 'POST':
        mes, anio = request.POST['periodo'].split("/")
        return HttpResponseRedirect(reverse('cuentas_corrientes:pdf_certificado', kwargs={'pk': pk, 'mes': mes,
                                                                                          'anio': anio}))
    return render(request, 'cuentaCorriente/cc_detail.html', {'cuenta': cuenta,
                                                              'detalles': DetalleCC.objects.filter(cc=cuenta)})


def get_monto(reinspeccion):
    precios = ReinspeccionPrecios.objects.get()
    monto = precios.precio_min

    if reinspeccion.total_kg > precios.kg_min:
        monto += reinspeccion.total_kg * precios.precio_kg

    return monto


def agrupar_reinspecciones(cc, mes, anio):
    reinspecciones = []
    detalles = DetalleCC.objects.filter(cc=cc, reinspeccion__fecha__month=mes, reinspeccion__fecha__year=anio)\
        .order_by('reinspeccion__fecha')
    for detalle in detalles:
        productos = ReinspeccionProducto.objects.filter(reinspeccion=detalle.reinspeccion)
        reinspecciones.append({'reinspeccion': detalle.reinspeccion, 'subtotal': get_monto(detalle.reinspeccion),
                               'productos': productos})
    return reinspecciones


class PdfCertificado(LoginRequiredMixin, PDFTemplateView):
    template_name = 'cuentaCorriente/certificado_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk, mes, anio):
        cc = CuentaCorriente.objects.get(pk=pk)
        locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')
        reinspecciones = agrupar_reinspecciones(cc, mes, anio)
        return super(PdfCertificado, self).get_context_data(
            cc=cc,
            reinspecciones=reinspecciones,
            periodo=calendar.month_name[int(mes)] + " " + str(anio),
            total_kilos=sum(item['reinspeccion'].total_kg for item in reinspecciones),
            total_monto=sum(item['subtotal'] for item in reinspecciones)
        )


'''
REINSPECCIONES
'''


@login_required(login_url='login')
def lista_reinspeccion(request):
    return render(request, 'reinspeccion/reinspeccion_list.html', {'listado': Reinspeccion.objects.all()})


@login_required(login_url='login')
def alta_reinspeccion(request):
    if request.method == 'POST':
        form = ReinspeccionForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        servicio = 'Reinspeccion Veterinaria'
        if form.is_valid():
            reinspeccion = form.save(commit=False)
            reinspeccion.detalles = False
            reinspeccion.save()
            importe = calculo_importe(reinspeccion.total_kg)
            if request.POST['optradio'] == 'previa':
                if detalle_mov_form.is_valid():
                    detalle_mov = detalle_mov_form.save(commit=False)
                    detalle_mov.completar_monto(importe, servicio, reinspeccion)
                    log_crear(request.user.id, reinspeccion, servicio)
                    return redirect('reinspecciones:lista_reinspecciones')
            else:
                if mov_form.is_valid():
                    mov = mov_form.save()
                    detalle_mov = pd_m.DetalleMovimiento(movimiento=mov)
                    detalle_mov.completar_monto(importe, servicio, reinspeccion)
                    log_crear(request.user.id, reinspeccion, servicio)
                    return redirect('reinspecciones:lista_reinspecciones')
    else:
        form = ReinspeccionForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'reinspeccion/reinspeccion_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                                   'mov_form': mov_form})


def calculo_importe(total_kg):
    precios = ReinspeccionPrecios.objects.get()
    monto = precios.precio_min
    if total_kg > precios.kg_min:
        monto += total_kg * precios.precio_kg
    return monto


@login_required(login_url='login')
def carga_productos(request, reinspeccion_pk):
    producto_form = ReinspeccionProductoForm
    mensaje = ''
    productos = []
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
            return redirect('reinspecciones:lista_reinspecciones')
    else:
        if 'productos' in request.session:
            del request.session['productos']
        request.session['productos'] = []
    return render(request, 'reinspeccion/carga_productos.html', {'producto_form': producto_form, 'mensaje': mensaje,
                                                                 'reinspeccion': Reinspeccion.objects.get(pk=reinspeccion_pk),
                                                                 'productos': productos})


@login_required(login_url='login')
def alta_reinspeccion_cc(request):
    producto_form = ReinspeccionProductoForm
    productos = []
    if request.method == 'POST':
        form = ReinspeccionCCForm(request.POST)
        servicio = 'Reinspeccion Veterinaria'
        if 'productos' in request.session:
            productos = request.session['productos']
        if form.is_valid():
            reinspeccion = form.save(commit=False)
            reinspeccion.detalles = True
            reinspeccion.save()
            alta_productos(request, reinspeccion)
            cc = CuentaCorriente.objects.get(abastecedor=reinspeccion.abastecedor)
            detalle = DetalleCC(reinspeccion=reinspeccion, cc=cc)
            detalle.save()
            log_crear(request.user.id, reinspeccion, servicio)
            return redirect('reinspecciones:lista_reinspecciones')
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


def alta_productos(request, reinspeccion):
    for producto in request.session['productos']:
        prod = Producto.objects.get(nombre=producto['producto']['nombre'])
        item = ReinspeccionProducto(producto=prod, kilo_producto=producto['kilo_producto'], reinspeccion=reinspeccion)
        item.save()
    reinspeccion_prod = ReinspeccionProducto.objects.filter(reinspeccion=reinspeccion)
    precios = ReinspeccionPrecios.objects.get()

    total_kg = 0
    monto = precios.precio_min

    for r in reinspeccion_prod:
        total_kg += r.kilo_producto
    if total_kg > precios.kg_min:
        monto += total_kg * precios.precio_kg

    reinspeccion.total_kg = total_kg
    reinspeccion.save()
    return monto


@login_required(login_url='login')
def lista_productos(request, reinspeccion_pk):
    reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
    referer = request.META.get('HTTP_REFERER')
    if 'detalle' in referer:
        url_return = 'cuentas_corrientes:detalle_cc'
    else:
        url_return = 'reinspecciones:lista_reinspecciones'
    return render(request, 'reinspeccion/producto_list.html', {'reinspeccion_pk': reinspeccion_pk,
                                                               'total_kg': reinspeccion.total_kg,
                                                               'url_return': url_return,
                                                               'id_return': referer.split('/')[-1],
                                                               'listado': ReinspeccionProducto.objects.filter(reinspeccion=reinspeccion)})


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


class PdfVehiculo(LoginRequiredMixin, PDFTemplateView):
    template_name = 'vehiculo/vehiculo_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        return super(PdfVehiculo, self).get_context_data(
            vehiculo=Vehiculo.objects.get(pk=pk)
        )


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
        return proximo_vencimiento.replace(day=calendar.monthrange(proximo_vencimiento.year, proximo_vencimiento.month)[1])


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
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if form.is_valid() & detalle_mov_form.is_valid():
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
                if detalle_mov_form.is_valid():
                    detalle_mov = detalle_mov_form.save(commit=False)
                    detalle_mov.importe = importe
                    detalle_mov.descripcion = str(servicio) + " | N° " + str(desinfeccion.id)
                    detalle_mov.servicio = str(servicio)
                    detalle_mov.save()
                    log_crear(request.user.id, desinfeccion, 'Desinfeccion')
                    return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=pk_vehiculo))
            else:
                if mov_form.is_valid():
                    mov = form.save()
                    detalle_mov = pd_m.DetalleMovimiento(movimiento=mov)
                    detalle_mov.importe = importe
                    detalle_mov.descripcion = str(servicio) + " | N° " + str(desinfeccion.id)
                    detalle_mov.servicio = str(servicio)
                    detalle_mov.save()
                    log_crear(request.user.id, desinfeccion, 'Desinfeccion')
                    return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=pk_vehiculo))

    else:
        form = DesinfeccionForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'desinfeccion/desinfeccion_form.html', {'estado': estado, 'vehiculo': vehiculo,
                                                                   'form': form, 'detalle_mov_form': detalle_mov_form,
                                                                   'mov_form': mov_form})


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
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        pago_diferido_form = PagoDiferidoForm(request.POST)
        if form.is_valid():
            servicio = "Fumigacion, desinfeccion, desratizacion"
            if request.POST['radio_tipo_pago'] == 'normal':
                if request.POST['optradio'] == 'previa':
                    if detalle_mov_form.is_valid():
                        control_plaga = form.save()
                        pd_v.movimiento_previo(request, detalle_mov_form, servicio, control_plaga,
                                               'Analisis de Triquinosis')
                        return redirect('controles_plagas:lista_controles_plagas')
                else:
                    if mov_form.is_valid():
                        control_plaga = form.save()
                        pd_v.nuevo_movimiento(request, mov_form, servicio, control_plaga, 'Analisis de Triquinosis')
                        return redirect('controles_plagas:lista_controles_plagas')
            else:
                if pago_diferido_form.is_valid():
                    control_plaga = form.save(commit=False)
                    control_plaga.pagado = False
                    control_plaga.save()
                    pago = pago_diferido_form.save(commit=False)
                    pago.detalles(servicio, control_plaga)
                    log_crear(request.user.id, control_plaga, 'Control de Plagas')
                    return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ControlDePlagaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
        pago_diferido_form = PagoDiferidoForm
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                                    'pago_diferido_form': pago_diferido_form,
                                                                    'mov_form': mov_form})


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
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if request.POST['optradio'] == 'previa':
            if detalle_mov_form.is_valid():
                detalle_mov = detalle_mov_form.save(commit=False)
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
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'controlPlaga/pago_control_form.html', {'detalle_mov_form': detalle_mov_form,
                                                                   'mov_form': mov_form})


@login_required(login_url='login')
def estadisticas_td(request):
    rango_form = dp_f.RangoAnioForm
    years = [timezone.now().year]
    if request.method == 'POST':
        rango_form = dp_f.RangoAnioForm(request.POST)
        if rango_form.is_valid():
            years = range(int(rango_form.cleaned_data['anio_hasta']),
                          int(rango_form.cleaned_data['anio_desde']) - 1, -1)

    des_tr = {}  # desinfeccion taxi/remis
    des_escolares = {}
    des_tsa = {}
    des_colectivos = {}

    for year in years:
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
        dic[k] = (v, float("{0:.2f}".format(v*100/total_general)))

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
    ord_dict_reinspeccion_prod = collections.OrderedDict(sorted(dict_reinspeccion_prod.iteritems(), key=lambda (k, v): (k, v)))  # Ordena los servicios por importe

    label_reinspeccion = ord_dict_reinspeccion_prod.keys()  # indistinto para los datos (tienen la misma clave)
    datos_reinspecciones = ord_dict_reinspeccion_prod.values()

    for k, v in ord_dict_reinspeccion_prod.items():
        ord_dict_reinspeccion_prod[k] = (v, float("{0:.2f}".format(v*100/total_general)))

    context = {
        'rango_form': rango_form,
        'dict': ord_dict_reinspeccion_prod,
        'total_general': total_general,
        # datos y etiquetas
        'lista_labels': json.dumps([label_reinspeccion]),
        'lista_datos': json.dumps([{'Productos': datos_reinspecciones}])
    }
    return render(request, "estadistica/estadisticas_reinspeccion.html", context)
