# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from personas import forms as f
from .forms import *
from .choices import *
from parte_diario_caja import forms as pd_f
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from desarrollo_patagonia.utils import *
from django.views.generic.detail import DetailView
from django.utils import timezone

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
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Abasto')
        if form.is_valid() & detalle_mov_form.is_valid():
            abastecedor = form.save()
            detalle_mov_diario = detalle_mov_form.save(commit=False)
            detalle_mov_diario.descripcion = str(detalle_mov_diario.servicio) + " N° " + str(abastecedor.id)
            detalle_mov_diario.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor')
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = AbastecedorForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(tipo='Abasto')
    return render(request, 'abastecedor/abastecedor_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form})


@login_required(login_url='login')
def nuevo_abastecedor_particular(request):
    if request.method == 'POST':
        form = f.AltaPersonaFisicaForm(request.POST)
        domicilio_form = f.DomicilioForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Abasto')
        if form.is_valid() & domicilio_form.is_valid() & detalle_mov_form.is_valid():
            responsable = form.save(commit=False)
            responsable.domicilio = domicilio_form.save()
            responsable.save()
            abastecedor = Abastecedor(responsable=responsable)
            abastecedor.save()
            detalle_mov_diario = detalle_mov_form.save(commit=False)
            detalle_mov_diario.descripcion = str(detalle_mov_diario.servicio) + " N° " + str(abastecedor.pk)
            detalle_mov_diario.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor - Particular')
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = f.AltaPersonaFisicaForm
        domicilio_form = f.DomicilioForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(tipo='Abasto')
    return render(request, 'abastecedor/nuevo_abastecedor_form.html', {'form': form, 'domicilio_form': domicilio_form,
                                                                       'detalle_mov_form': detalle_mov_form})


@login_required(login_url='login')
def nuevo_abastecedor_empresa(request):
    if request.method == 'POST':
        form = f.AltaPersonaJuridicaForm(request.POST)
        domicilio_form = f.DomicilioForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Abasto')
        if form.is_valid() & domicilio_form.is_valid() & detalle_mov_form.is_valid():
            responsable = form.save(commit=False)
            responsable.domicilio = domicilio_form.save()
            responsable.save()
            abastecedor = Abastecedor(responsable=responsable)
            abastecedor.save()
            detalle_mov_diario = detalle_mov_form.save(commit=False)
            detalle_mov_diario.descripcion = str(detalle_mov_diario.servicio) + " N° " + str(abastecedor.pk)
            detalle_mov_diario.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor - Empresa')
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = f.AltaPersonaJuridicaForm
        domicilio_form = f.DomicilioForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(tipo='Abasto')
    return render(request, 'abastecedor/nuevo_abastecedor_form.html', {'form': form, 'domicilio_form': domicilio_form,
                                                                       'detalle_mov_form': detalle_mov_form})


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
    return render(request, 'cuentaCorriente/cc_list.html', {'listado': DetalleCC.objects.all()})


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
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Reinspeccion')
            return redirect('reinspecciones:lista_reinspecciones')
    else:
        form = ReinspeccionForm
    return render(request, 'reinspeccion/reinspeccion_form.html', {'form': form})


@login_required(login_url='login')
def baja_reinspeccion(request, reinspeccion_pk):
    reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
    log_eliminar(request.user.id, reinspeccion, 'Reinspeccion')
    reinspeccion.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_reinspeccion(request, reinspeccion_pk):
    reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
    if request.method == 'POST':
        form = ModificacionReinspeccionForm(request.POST, instance=reinspeccion)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Reinspeccion')
            return redirect('reinspecciones:lista_reinspecciones')
    else:
        form = ModificacionReinspeccionForm(instance=reinspeccion)
    return render(request, 'reinspeccion/reinspeccion_form.html', {'form': form, 'modificacion': True})


@login_required(login_url='login')
def reinspeccion_cc(request, reinspeccion_pk):
    reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
    cc = CuentaCorriente.objects.get()
    reinspeccion_prod = ReinspeccionProducto.objects.filter(reinspeccion=reinspeccion)

    total_kg = 0
    minimo = 30  # kilaje minimo para probar....
    tarifa = 0.25  # precio por kilaje

    for r in reinspeccion_prod:
        total_kg += r.kilo_producto

    if total_kg <= minimo:
        cc.saldo = 55
    else:
        cc.saldo = 55 + (total_kg * tarifa)
    cc.save()

    Reinspeccion.objects.filter(pk=reinspeccion_pk).update(cc=cc)  # actualizacion reinspeccion
    reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)

    detalle_cc = DetalleCC()
    detalle_cc.cc = cc
    detalle_cc.detalle = reinspeccion
    detalle_cc.save()

    return render(request, 'reinspeccion/reinspeccion_list.html', {'listado': Reinspeccion.objects.all()})


@login_required(login_url='login')
def lista_productos(request, reinspeccion_pk):
    return render(request, 'reinspeccion/producto_list.html', {'reinspeccion_pk': reinspeccion_pk,
                                                               'listado': ReinspeccionProducto.objects.filter(
                                                                   reinspeccion__pk=reinspeccion_pk)})


#nuevo producto en el sistema, sin estar relacionado con la inspeccion
class AltaProducto(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = Producto
    form_class = AltaProductoForm
    template_name = "reinspeccion/simple_producto_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def nuevo_producto(request, reinspeccion_pk):
    if request.method == 'POST':
        form = ReinspeccionProductoForm(request.POST, reinspeccion_pk=reinspeccion_pk)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
            producto.save()
            log_crear(request.user.id, producto, 'Producto de Reinspeccion')
            return HttpResponseRedirect(reverse('reinspecciones:lista_productos', args=reinspeccion_pk))
    else:
        form = ReinspeccionProductoForm
    return render(request, "reinspeccion/producto_form.html", {'reinspeccion_pk': reinspeccion_pk, 'form': form})


@login_required(login_url='login')
def baja_producto(request, pk):
    producto = ReinspeccionProducto.objects.get(pk=pk)
    log_eliminar(request.user.id, producto, 'Producto de Reinspeccion')
    producto.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificar_producto(request, pk, reinspeccion_pk):
    reinspeccion_producto = ReinspeccionProducto.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionReinspeccionProductoForm(request.POST, instance=reinspeccion_producto)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Producto de Reinspeccion')
            return HttpResponseRedirect(reverse('reinspecciones:lista_productos',
                                                kwargs={'reinspeccion_pk': reinspeccion_pk}))
    else:
        form = ModificacionReinspeccionProductoForm(instance=reinspeccion_producto)
        return render(request, 'reinspeccion/producto_form.html', {'form': form, 'reinspeccion_pk': reinspeccion_pk,
                                                                   'modificacion': True})


'''
VEHICULO
'''


@login_required(login_url='login')
def get_rubros_json(request, id_categoria):
    return JsonResponse({
        'Categoria_A': Categoria_A,
        'Categoria_B': Categoria_B,
        'Categoria_C': Categoria_C,
        'Categoria_D': Categoria_D,
        'Categoria_E': Categoria_E
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
            print (vehiculo.categoria)
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
        if form.is_valid():
            desinfeccion = form.save(commit=False)
            desinfeccion.vehiculo = vehiculo
            desinfeccion.quincena = 'Primera' if desinfeccion.fecha_realizacion.day <= 15 else 'Segunda'
            desinfeccion.proximo_vencimiento = get_vencimiento(desinfeccion.fecha_realizacion)
            if estado == 'Atrasado':
                desinfeccion.infraccion = True
            desinfeccion.save()
            log_crear(request.user.id, desinfeccion, 'Desinfeccion')
            return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=pk_vehiculo))
    else:
        form = DesinfeccionForm
    return render(request, 'desinfeccion/desinfeccion_form.html', {'estado': estado, 'pk_vehiculo': pk_vehiculo,
                                                                   'tipo_vehiculo': vehiculo.tipo_vehiculo,
                                                                   'form': form})


@login_required(login_url='login')
def baja_desinfeccion(request, pk):
    desinfeccion = Desinfeccion.objects.get(pk=pk)
    log_eliminar(request.user.id, desinfeccion, 'Desinfeccion')
    desinfeccion.delete()
    return HttpResponse()


def modificar_desinfeccion(request, pk_vehiculo, pk):
    desinfeccion = Desinfeccion.objects.get(pk=pk)
    if request.method == 'POST':
        form = DesinfeccionForm(request.POST, instance=desinfeccion)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Desinfeccion')
            return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=pk_vehiculo))
    else:
        form = DesinfeccionForm(instance=desinfeccion)
    return render(request, 'desinfeccion/desinfeccion_form.html', {'form': form, 'pk_vehiculo': pk_vehiculo,
                                                                   'modificacion': True})


'''
CONTROLES DE PLAGAS
'''


@login_required(login_url='login')
def lista_controles_plaga(request):
    return render(request, 'controlPlaga/control_plaga_list.html', {'listado': ControlDePlaga.objects.all()})


@login_required(login_url='login')
def alta_control_plaga(request):
    if request.method == 'POST':
        form = ControlDePlagaForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Control de Plagas')
        if form.is_valid() & detalle_mov_form.is_valid():
            control_plaga = form.save()
            detalle_mov_diario = detalle_mov_form.save(commit=False)
            detalle_mov_diario.descripcion = str(detalle_mov_diario.servicio) + " N° " + str(control_plaga.id)
            detalle_mov_diario.save()
            log_crear(request.user.id, control_plaga, 'Control de Plagas')
            return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ControlDePlagaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(tipo='Control de Plagas')
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form})


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
