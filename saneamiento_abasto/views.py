# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from personas import forms as f
from .forms import *
from .filters import *
from .choices import *
from parte_diario_caja import forms as pd_f
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from desarrollo_patagonia.utils import *
from django.views.generic.edit import UpdateView


'''
ABASTECEDORES
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
def lista_abastecedor(request):
    lista_abastecedores = Abastecedor.objects.all()
    filtro_abastecedores = AbastecedorListFilter(request.GET, queryset=lista_abastecedores)
    return render(request, 'abastecedor/abastecedor_list.html', {'filter': filtro_abastecedores})


def alta_abastecedor(request):
    if request.method == 'POST':
        form = AbastecedorForm(request.POST)
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Abasto')
        if form.is_valid() & mov_diario_form.is_valid() & detalle_mov_diario_form.is_valid():
            abastecedor = form.save()
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " - " + str(abastecedor.id)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip,
                                               abastecedor.responsable)
            detalle_mov_diario.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor')
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = AbastecedorForm
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Abasto')
    return render(request, 'abastecedor/abastecedor_form.html', {'form': form, 'mov_diario_form': mov_diario_form,
                                                                 'detalle_mov_diario_form': detalle_mov_diario_form})


def nuevo_abastecedor_particular(request):
    if request.method == 'POST':
        responsable_form = f.AltaPersonaFisicaForm(request.POST)
        domicilio_form = f.DomicilioForm(request.POST)
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Abasto')
        if responsable_form.is_valid() & domicilio_form.is_valid() & mov_diario_form.is_valid() & \
                detalle_mov_diario_form.is_valid():
            responsable = responsable_form.save(commit=False)
            responsable.domicilio = domicilio_form.save()
            responsable.save()
            abastecedor = Abastecedor(responsable=responsable)
            abastecedor.save()
            print (abastecedor)
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " - " + str(abastecedor.id)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip,
                                               abastecedor.responsable)
            detalle_mov_diario.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor - Particular')
            return redirect('abastecedores:lista_abastecedores')
    else:
        responsable_form = f.AltaPersonaFisicaForm
        domicilio_form = f.DomicilioForm
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Abasto')
    return render(request, 'abastecedor/nuevo_abastecedor_form.html', {'responsable_form': responsable_form,
                                                                       'domicilio_form': domicilio_form,
                                                                       'mov_diario_form': mov_diario_form,
                                                                       'detalle_mov_diario_form': detalle_mov_diario_form
                                                                       })


def nuevo_abastecedor_empresa(request):
    if request.method == 'POST':
        responsable_form = f.AltaPersonaJuridicaForm(request.POST)
        domicilio_form = f.DomicilioForm(request.POST)
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Abasto')
        if responsable_form.is_valid() & domicilio_form.is_valid() & mov_diario_form.is_valid() & \
                detalle_mov_diario_form.is_valid():
            responsable = responsable_form.save(commit=False)
            responsable.domicilio = domicilio_form.save()
            responsable.save()
            abastecedor = Abastecedor(responsable=responsable)
            abastecedor.save()
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " - " + str(abastecedor.pk)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip,
                                               abastecedor.responsable)
            detalle_mov_diario.save()
            log_crear(request.user.id, abastecedor, 'Abastecedor - Empresa')
            return redirect('abastecedores:lista_abastecedores')
    else:
        responsable_form = f.AltaPersonaJuridicaForm
        domicilio_form = f.DomicilioForm
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Abasto')
    return render(request, 'abastecedor/nuevo_abastecedor_form.html', {'responsable_form': responsable_form,
                                                                       'domicilio_form': domicilio_form,
                                                                       'mov_diario_form': mov_diario_form,
                                                                       'detalle_mov_diario_form': detalle_mov_diario_form
                                                                       })


@login_required(login_url='login')
def baja_abastecedor(request, pk):
    abastecedor = Abastecedor.objects.get(pk=pk)
    log_crear(request.user.id, abastecedor, 'Abastecedor')
    abastecedor.delete()
    return HttpResponse()


'''
REINSPECCIONES
'''


@login_required(login_url='login')
def lista_reinspeccion(request):
    lista_reinspecciones = Reinspeccion.objects.all()
    filtro_reinspecciones = ReinspeccionListFilter(request.GET, queryset=lista_reinspecciones)
    return render(request, 'reinspeccion/reinspeccion_list.html', {'filter': filtro_reinspecciones})


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
    log_crear(request.user.id, reinspeccion, 'Reinspeccion')
    reinspeccion.delete()
    return HttpResponse()


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


def lista_productos(request, reinspeccion_pk):
    listado_productos = ReinspeccionProducto.objects.filter(reinspeccion__pk=reinspeccion_pk)
    filtro_productos = ReinspeccionProductoListFilter(request.GET, queryset=listado_productos)
    return render(request, 'reinspeccion/producto_list.html', {'reinspeccion_pk': reinspeccion_pk,
                                                               'filter': filtro_productos})


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


def baja_producto(request, pk):
    producto = ReinspeccionProducto.objects.get(pk=pk)
    log_eliminar(request.user.id, producto, 'Producto de Reinspeccion')
    producto.delete()
    return HttpResponse()


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
def lista_vehiculo(request):
    listado_vehiculo = Vehiculo.objects.all()
    filtro_vehiculo = VehiculoListFilter(request.GET, queryset=listado_vehiculo)
    return render(request, 'vehiculo/vehiculo_list.html', {'filter': filtro_vehiculo})


class DetalleVehiculo(LoginRequiredMixin, DetailView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


def alta_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.rubro_vehiculo = request.POST['rubro_vehiculo']
            vehiculo.save()
            log_crear(request.user.id, vehiculo, 'Vehiculo')
            return redirect('vehiculo:lista_vehiculos')
    else:
        form = VehiculoForm
    return render(request, 'vehiculo/vehiculo_form.html', {'form': form})


def baja_vehiculo(request, pk):
    vehiculo = Vehiculo.objects.get(pk=pk)
    log_eliminar(request.user.id, vehiculo, 'Vehiculo')
    vehiculo.delete()
    return HttpResponse()


def modificacion_vehiculo(request, pk):
    vehiculo = Vehiculo.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificarVehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.rubro_vehiculo = request.POST['rubro_vehiculo']
            vehiculo.save()
            log_modificar(request.user.id, vehiculo, 'Vehiculo')
            return redirect('vehiculo:lista_vehiculos')
    else:
        form = ModificarVehiculoForm(instance=vehiculo)
    return render(request, 'vehiculo/vehiculo_form.html', {'tipo': vehiculo.tipo_vehiculo, 'form': form})


'''
DESINFECCIONES
'''


@login_required(login_url='login')
def lista_desinfecciones(request, pk_vehiculo):
    listado_desinfecciones = Desinfeccion.objects.all()
    filtro_desinfeccion = DesinfeccionListFilter(request.GET, queryset=listado_desinfecciones)
    # Tener en cuenta que en filter = TSA.
    return render(request, 'desinfeccion/desinfeccion_list.html', {'filter': filtro_desinfeccion,
                                                                   'pk_vehiculo': pk_vehiculo})


def nueva_desinfeccion(request, pk_vehiculo):
    if request.method == 'POST':
        form = DesinfeccionForm(request.POST)
        if form.is_valid():
            desinfeccion = form.save(commit=False)
            desinfeccion.vehiculo = Vehiculo.objects.get(pk=pk_vehiculo)
            desinfeccion.save()
            log_crear(request.user.id, desinfeccion, 'Desinfeccion')
            return HttpResponseRedirect(reverse('desinfecciones:lista_desinfecciones', args=pk_vehiculo))
    else:
        form = DesinfeccionForm
    return render(request, 'desinfeccion/desinfeccion_form.html', {'form': form, 'pk_vehiculo': pk_vehiculo})


def baja_desinfeccion(request, pk):
    desinfeccion = Desinfeccion.objects.get(pk=pk)
    log_eliminar(request.user.id, desinfeccion, 'Desinfeccion')
    desinfeccion.delete()
    return HttpResponse()


class ModificacionDesinfeccion(LoginRequiredMixin, UpdateView):
    model = Desinfeccion
    template_name = 'desinfeccion/desinfeccion_form.html'
    success_url = reverse_lazy('desinfecciones:lista_desinfecciones')
    form_class = DesinfeccionForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
CONTROLES DE PLAGAS
'''


@login_required(login_url='login')
def lista_controles_plaga(request):
    listado_controles_plaga = ControlDePlaga.objects.all()
    filtro_controles = ControlDePlagaListFilter(request.GET, queryset=listado_controles_plaga)
    return render(request, 'controlPlaga/control_plaga_list.html', {'filter': filtro_controles})


@login_required(login_url='login')
def alta_control_plaga(request):
    if request.method == 'POST':
        form = ControlDePlagaForm(request.POST)
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Control de Plagas')
        if form.is_valid() & mov_diario_form.is_valid() & detalle_mov_diario_form.is_valid():
            control_plaga = form.save()
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " - " + str(control_plaga.id)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip,
                                               control_plaga.responsable)
            detalle_mov_diario.save()
            log_crear(request.user.id, control_plaga, 'Control de Plagas')
            return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ControlDePlagaForm
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Control de Plagas')
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form, 'mov_diario_form': mov_diario_form,
                                                                    'detalle_mov_diario_form': detalle_mov_diario_form})


class DetalleControlPlaga(LoginRequiredMixin, DetailView):
    model = ControlDePlaga
    template_name = 'controlPlaga/control_plaga_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


def baja_control_plaga(request, pk):
    control_plaga = ControlDePlaga.objects.get(pk=pk)
    log_eliminar(request.user.id, control_plaga, 'Control de Plagas')
    control_plaga.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_control_plaga(request):
    if request.method == 'POST':
        form = ControlDePlagaForm(request.POST)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Control de Plagas')
            return redirect('controles_plagas:lista_controles_plagas')
    else:
        form = ControlDePlagaForm
    return render(request, 'controlPlaga/control_plaga_form.html', {'form': form})
