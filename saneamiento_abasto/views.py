# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from personas import forms as f
from .forms import *
from .filters import *
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)

'''
ABASTECEDORES
'''


@login_required(login_url='login')
def lista_abastecedor(request):
    lista_abastecedores = Abastecedor.objects.all()
    filtro_abastecedores = AbastecedorListFilter(request.GET, queryset=lista_abastecedores)
    return render(request, 'abastecedor/abastecedor_list.html', {'filter': filtro_abastecedores})


def alta_abastecedor(request):
    if request.method == 'POST':
        form = f.ListaPersonasFisicasForm(request.POST)
        if form.is_valid():
            persona = form.cleaned_data['persona']
            return HttpResponseRedirect(reverse('abastecedores:info_adicional_abastecedor', args=[persona.pk]))
    else:
        form = f.ListaPersonasFisicasForm
        return render(request, 'abastecedor/abastecedor_form.html', {'form': form})


def info_adicional_abastecedor(request, pk):
    if request.method == 'POST':
        form = AbastecedorAdicionalForm(request.POST)
        if form.is_valid():
            persona = m.PersonaFisica.objects.get(pk=pk)
            abastecedor = Abastecedor(personafisica_ptr=persona)
            empresa = form.cleaned_data['empresa']
            categoria = form.cleaned_data['categoria']
            rubro_abastecedor = form.cleaned_data['rubro_abastecedor']
            abastecedor.empresa = empresa
            abastecedor.categoria = categoria
            abastecedor.rubro_abastecedor = rubro_abastecedor
            abastecedor.save_base(raw=True)
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = AbastecedorAdicionalForm
    return render(request, 'abastecedor/info_adicional_form.html', {'form': form})


def nuevo_abastecedor(request):
    if request.method == 'POST':
        form = AbastecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = AbastecedorForm
    return render(request, 'abastecedor/nuevo_abastecedor_form.html', {'form': form})


class BajaAbastecedor(LoginRequiredMixin, DeleteView):
    model = Abastecedor
    template_name = 'abastecedor/abastecedor_confirm_delete.html'
    success_url = reverse_lazy('abastecedores:lista_abastecedores')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionAbastecedor(LoginRequiredMixin, UpdateView):
    model = Abastecedor
    template_name = 'abastecedor/abastecedor_form.html'
    success_url = reverse_lazy('abastecedores:lista_abastecedores')
    form_class = AbastecedorForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
REINSPECCIONES
'''


@login_required(login_url='login')
def lista_reinspeccion(request):
    lista_reinspecciones = Reinspeccion.objects.all()
    filtro_reinspecciones = ReinspeccionListFilter(request.GET, queryset=lista_reinspecciones)
    return render(request, 'reinspeccion/reinspeccion_list.html', {'filter': filtro_reinspecciones})


class AltaReinspeccion(LoginRequiredMixin, CreateView):
    model = Reinspeccion
    template_name = 'reinspeccion/reinspeccion_form.html'
    success_url = reverse_lazy('reinspecciones:lista_reinspecciones')
    form_class = ReinspeccionForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaReinspeccion(LoginRequiredMixin, DeleteView):
    model = Reinspeccion
    template_name = 'reinspeccion/reinspeccion_confirm_delete.html'
    success_url = reverse_lazy('reinspecciones:lista_reinspecciones')
    pk_url_kwarg = 'reinspeccion_pk'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionReinspeccion(LoginRequiredMixin, UpdateView):
    model = Reinspeccion
    template_name = 'reinspeccion/reinspeccion_form.html'
    success_url = reverse_lazy('reinspecciones:lista_reinspecciones')
    form_class = ReinspeccionForm
    pk_url_kwarg = 'reinspeccion_pk' #Si se cambia el nombre pk en la url se debe agregar este parámetro.
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


def lista_productos(request, reinspeccion_pk):
    lista_productos = ReinspeccionProducto.objects.filter(reinspeccion__pk=reinspeccion_pk)
    filtro_productos = ReinspeccionProductoListFilter(request.GET, queryset=lista_productos)
    return render(request, 'reinspeccion/producto_list.html', {'reinspeccion_pk': reinspeccion_pk,
                                                               'filter': filtro_productos})


def nuevo_producto(request, reinspeccion_pk):
    if request.method == 'POST':
        form = ReinspeccionProductoForm(request.POST, reinspeccion_pk=reinspeccion_pk)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.reinspeccion = Reinspeccion.objects.get(pk=reinspeccion_pk)
            producto.save()
            return HttpResponseRedirect(reverse('reinspecciones:lista_productos', args=reinspeccion_pk))
    else:
        form = ReinspeccionProductoForm
    return render(request, "reinspeccion/producto_form.html", {'reinspeccion_pk': reinspeccion_pk, 'form': form})


def borrar_producto(request, pk):
    producto = ReinspeccionProducto.objects.get(pk=pk)
    producto.delete()
    return HttpResponse()


def modificar_producto(request, pk, reinspeccion_pk):
        reinspeccion_producto = ReinspeccionProducto.objects.get(pk=pk)
        if request.method == 'POST':
            form = ReinspeccionProductoForm(request.POST, reinspeccion_pk=reinspeccion_pk)
            if form.is_valid():
                producto = form.cleaned_data['producto']
                kilo_producto = form.cleaned_data['kilo_producto']
                reinspeccion_producto.producto = producto
                reinspeccion_producto.kilo_producto = kilo_producto
                reinspeccion_producto.save()
                return HttpResponseRedirect(reverse('reinspecciones:lista_productos', kwargs={'reinspeccion_pk': reinspeccion_pk}))
        else:
            form = ReinspeccionProductoForm(initial={'producto': reinspeccion_producto.producto, 'kilo_producto': reinspeccion_producto.kilo_producto})
            url_return = 'reinspecciones:lista_productos'
            return render(request, 'reinspeccion/producto_form.html', {'form': form, 'reinspeccion_pk': reinspeccion_pk,
                                                                         'url_return': url_return})


'''
VEHICULO
'''


@login_required(login_url='login')
def lista_vehiculo(request):
    lista_vehiculo = Vehiculo.objects.all()
    filtro_vehiculo = VehiculoListFilter(request.GET, queryset=lista_vehiculo)
    return render(request, 'vehiculo/vehiculo_list.html', {'filter': filtro_vehiculo})


class DetalleVehiculo(LoginRequiredMixin, DetailView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaVehiculo(LoginRequiredMixin, CreateView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo_form.html'
    success_url = reverse_lazy('vehiculo:lista_vehiculos')
    form_class = VehiculoForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaVehiculo(LoginRequiredMixin, DeleteView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo_confirm_delete.html'
    success_url = reverse_lazy('vehiculo:lista_vehiculos')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionVehiculo(LoginRequiredMixin, UpdateView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo_form.html'
    success_url = reverse_lazy('vehiculo:lista_vehiculos')
    form_class = VehiculoForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
DESINFECCIONES
'''


@login_required(login_url='login')
def lista_desinfecciones(request):
    lista_desinfecciones = Desinfeccion.objects.all()
    filtro_desinfeccion = DesinfeccionListFilter(request.GET, queryset=lista_desinfecciones)
    # Tener en cuenta que en filter = TSA.
    return render(request, 'desinfeccion/desinfeccion_list.html', {'filter': filtro_desinfeccion})


class AltaDesinfeccion(LoginRequiredMixin, CreateView):
    model = Desinfeccion
    template_name = 'desinfeccion/desinfeccion_form.html'
    success_url = reverse_lazy('desinfecciones:lista_desinfecciones')
    form_class = DesinfeccionForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaDesinfeccion(LoginRequiredMixin, DeleteView):
    model = Desinfeccion
    template_name = 'desinfeccion/desinfeccion_confirm_delete.html'
    success_url = reverse_lazy('desinfecciones:lista_desinfecciones')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


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
    lista_controles_plaga = ControlDePlaga.objects.all()
    filtro_controles = ControlDePlagaListFilter(request.GET, queryset=lista_controles_plaga)
    return render(request, 'controlPlaga/control_plaga_list.html', {'filter': filtro_controles})


class DetalleControlPlaga(LoginRequiredMixin, DetailView):
    model = ControlDePlaga
    template_name = 'controlPlaga/control_plaga_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaControlPlaga(LoginRequiredMixin, CreateView):
    model = ControlDePlaga
    template_name = 'controlPlaga/control_plaga_form.html'
    success_url = reverse_lazy('controles_plagas:lista_controles_plagas')
    form_class = ControlDePlagaForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaControlPlaga(LoginRequiredMixin, DeleteView):
    model = ControlDePlaga
    template_name = 'controlPlaga/control_plaga_confirm_delete.html'
    success_url = reverse_lazy('controles_plagas:lista_controles_plagas')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionControlPlaga(LoginRequiredMixin, UpdateView):
    model = ControlDePlaga
    template_name = 'controlPlaga/control_plaga_form.html'
    success_url = reverse_lazy('controles_plagas:lista_controles_plagas')
    form_class = ControlDePlagaForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
