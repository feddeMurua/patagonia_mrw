# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.shortcuts import render
import datetime
from .forms import *
from .filters import *
from .models import *
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)


'''
ANALISIS
'''

@login_required(login_url='login')
def lista_analisis(request):
    lista_analisis = Analisis.objects.all()
    filtro_analisis = AnalisisListFilter(request.GET, queryset=lista_analisis)    
    return render(request, 'analisis/analisis_list.html', {'filter': filtro_analisis})


class AltaAnalisis(LoginRequiredMixin, CreateView):
    model = Analisis
    template_name = 'analisis/analisis_form.html'
    success_url = reverse_lazy('analisis:lista_analisis')
    form_class = AnalisisForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaAnalisis(LoginRequiredMixin, DeleteView):
    model = Analisis
    template_name = 'analisis/analisis_confirm_delete.html'
    success_url = reverse_lazy('analisis:lista_analisis')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class DetalleAnalisis(LoginRequiredMixin, DetailView):
    model = Analisis
    template_name = 'analisis/analisis_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
HABILITACION CRIADERO DE CERDOS
'''

@login_required(login_url='login')
def lista_habilitaciones(request):
    lista_habilitaciones = HabilitacionCriaderoCerdos.objects.all()
    filtro_habilitaciones = HabilitacionListFilter(request.GET, queryset=lista_habilitaciones)    
    return render(request, 'habilitacion/habilitacion_list.html', {'filter': filtro_habilitaciones})


class AltaHabilitacion(LoginRequiredMixin, CreateView):
    model = HabilitacionCriaderoCerdos
    template_name = 'habilitacion/habilitacion_form.html'
    success_url = reverse_lazy('habilitacion:lista_habilitaciones')
    form_class = HabilitacionForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
ESTERILIZACION
'''

@login_required(login_url='login')
def lista_esterilizaciones(request):
    lista_esterilizaciones = Esterilizacion.objects.all()
    filtro_esterilizaciones = EsterilizacionListFilter(request.GET, queryset=lista_esterilizaciones)    
    return render(request, 'esterilizacion/esterilizacion_list.html', {'filter': filtro_esterilizaciones})


class AltaEsterilizacion(LoginRequiredMixin, CreateView):
    model = Esterilizacion
    template_name = 'esterilizacion/esterilizacion_form.html'
    success_url = reverse_lazy('esterilizacion:lista_esterilizaciones')
    form_class = EsterilizacionForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
