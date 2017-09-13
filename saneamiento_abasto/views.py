# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from .models import *
from .forms import *
from .filters import *
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
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
        form = ListaPersonasFisicasForm(request.POST)
        if form.is_valid():
            persona = form.cleaned_data['persona']
            return HttpResponseRedirect(reverse('abastecedores:razon_social_abastecedor', args=[persona.pk]))
    else:
        form = ListaPersonasFisicasForm
        return render(request, 'abastecedor/abastecedor_form.html', {'form':form})


def razon_social_abastecedor(request, pk):
    if request.method == 'POST':
        form = RazonSocialForm(request.POST)
        if form.is_valid():
            persona = m.PersonaFisica.objects.get(pk=pk)
            abastecedor = Abastecedor(personafisica_ptr=persona)
            razon_social = form.cleaned_data['razon_social']
            abastecedor.empresa = razon_social
            abastecedor.save_base(raw=True)
            return redirect('abastecedores:lista_abastecedores')
    else:
        form = RazonSocialForm()
    return render(request, 'abastecedor/razon_social_form.html', {'form': form})


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
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionReinspeccion(LoginRequiredMixin, UpdateView):
    model = Reinspeccion
    template_name = 'reinspeccion/reinspeccion_form.html'
    success_url = reverse_lazy('reinspecciones:lista_reinspecciones')
    form_class = ReinspeccionForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


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
    filtro_desinfeccion = DesinfeccionListFilter(request.GET, queryset=lista_desinfecciones) #Tener en cuenta que en filter = vehiculo.
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
