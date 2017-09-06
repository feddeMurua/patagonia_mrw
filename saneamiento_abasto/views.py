# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from .models import *
from .forms import *
from .filters import *
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


class AltaAbastecedor(LoginRequiredMixin, CreateView):
    model = Abastecedor
    template_name = 'abastecedor/abastecedor_form.html'
    success_url = reverse_lazy('abastecedores:lista_abastecedores')
    form_class = AbastecedorForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


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
