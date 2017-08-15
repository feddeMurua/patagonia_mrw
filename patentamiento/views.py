# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from .forms import *
from .filters import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    )

'''
PATENTES
'''


@login_required(login_url='login')
def lista_patente(request):
    lista_patentes = Patente.objects.all()
    filtro_patentes = PatenteListFilter(request.GET, queryset=lista_patentes)    
    return render(request, 'patente/patente_list.html', {'filter': filtro_patentes})


class AltaPatente(LoginRequiredMixin, CreateView):
    model = Patente
    template_name = 'patente/patente_form.html'
    success_url = reverse_lazy('patentes:lista_patentes')
    form_class = PatenteForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaPatente(LoginRequiredMixin, DeleteView):
    model = Patente
    template_name = 'patente/patente_confirm_delete.html'
    success_url = reverse_lazy('patentes:lista_patentes')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionPatente(LoginRequiredMixin, UpdateView):
    model = Patente
    template_name = 'patente/patente_form.html'
    success_url = reverse_lazy('patentes:lista_patentes')
    fields = ['persona', 'observaciones']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


'''
MASCOTAS



class DetalleMascota(LoginRequiredMixin, DetailView):
    model = Mascota
    template_name = 'mascota/mascota_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaMascota(LoginRequiredMixin, CreateView):
    model = Mascota
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascotas:lista_mascotas')
    form_class = MascotaForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaMascota(LoginRequiredMixin, DeleteView):
    model = Mascota
    template_name = 'mascota/mascota_confirm_delete.html'
    success_url = reverse_lazy('mascotas:lista_mascotas')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionMascota(LoginRequiredMixin, UpdateView):
    model = Mascota
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascotas:lista_mascotas')
    fields = ['nombre', 'pelaje', 'raza', 'fecha_nacimiento', 'sexo']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

'''