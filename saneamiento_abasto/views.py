# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from .models import *
from .forms import *
from .filters import *
from django.views.generic.detail import DetailView
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
TSA
'''

@login_required(login_url='login')
def lista_tsa(request):
    lista_tsa = Tsa.objects.all()
    filtro_tsa = TsaListFilter(request.GET, queryset=lista_tsa)
    return render(request, 'tsa/tsa_list.html', {'filter': filtro_tsa})


class DetalleTsa(LoginRequiredMixin, DetailView):
    model = Tsa
    template_name = 'tsa/tsa_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaTsa(LoginRequiredMixin, CreateView):
    model = Tsa
    template_name = 'tsa/tsa_form.html'
    success_url = reverse_lazy('tsa:lista_tsa')
    form_class = TsaForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaTsa(LoginRequiredMixin, DeleteView):
    model = Tsa
    template_name = 'tsa/tsa_confirm_delete.html'
    success_url = reverse_lazy('tsa:lista_tsa')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionTsa(LoginRequiredMixin, UpdateView):
    model = Tsa
    template_name = 'tsa/tsa_form.html'
    success_url = reverse_lazy('tsa:lista_tsa')
    form_class = TsaForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
TPP
'''


@login_required(login_url='login')
def lista_tpp(request):
    lista_tpp = Tpp.objects.all()
    filtro_tpp = TppListFilter(request.GET, queryset=lista_tpp) #Tener en cuenta que en filter = TSA porque son iguales los modelos.
    return render(request, 'tpp/tpp_list.html', {'filter': filtro_tpp})


class DetalleTpp(LoginRequiredMixin, DetailView):
    model = Tpp
    template_name = 'tpp/tpp_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaTpp(LoginRequiredMixin, CreateView):
    model = Tpp
    template_name = 'tpp/tpp_form.html'
    success_url = reverse_lazy('tpp:lista_tpp')
    form_class = TppForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaTpp(LoginRequiredMixin, DeleteView):
    model = Tpp
    template_name = 'tpp/tpp_confirm_delete.html'
    success_url = reverse_lazy('tpp:lista_tpp')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionTpp(LoginRequiredMixin, UpdateView):
    model = Tpp
    template_name = 'tpp/tpp_form.html'
    success_url = reverse_lazy('tpp:lista_tpp')
    form_class = TppForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
DESINFECCIONES
'''

@login_required(login_url='login')
def lista_desinfecciones(request):
    lista_desinfecciones = Desinfeccion.objects.all()
    filtro_desinfeccion = DesinfeccionListFilter(request.GET, queryset=lista_desinfecciones) #Tener en cuenta que en filter = TSA.
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
