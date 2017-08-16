# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from easy_pdf.views import PDFTemplateView
from django.shortcuts import render, redirect
import datetime
from .forms import *
from .filters import *
from .models import *
from django.views.generic.detail import DetailView
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
    fecha_hoy = datetime.date.today()
    return render(request, 'analisis/analisis_list.html', {'fecha_hoy': fecha_hoy, 'filter': filtro_analisis})


def alta_analisis(request):
    if request.method == 'POST':
        analisis_form = AnalisisForm(request.POST)
        porcino_formset = PorcinoFormSet(request.POST)
        if analisis_form.is_valid() & porcino_formset.is_valid():
            analisis = analisis_form.save()
            for porcino_form in porcino_formset:
                porcino = porcino_form.save(commit=False)
                porcino.analisis = analisis
                porcino.save()
            return redirect('analisis:lista_analisis')
    else:
        form = AnalisisForm()
        formset = PorcinoFormSet()
        return render(request, 'analisis/analisis_form.html', {"form": form, "formset": formset})


class BajaAnalisis(LoginRequiredMixin, DeleteView):
    model = Analisis
    template_name = 'analisis/analisis_confirm_delete.html'
    success_url = reverse_lazy('analisis:lista_analisis')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


def detalle_analisis(request, pk):
    analisis = Analisis.objects.get(pk=pk)
    porcinos = Porcino.objects.filter(analisis__pk=pk)
    return render(request, 'analisis/analisis_detail.html', {'analisis': analisis, 'porcinos': porcinos})


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


class PdfHabilitacion(PDFTemplateView):
    template_name = 'habilitacion/habilitacion_pdf.html'

    def get_context_data(self, pk):
        habilitacion = HabilitacionCriaderoCerdos.objects.get(pk=pk)
        return super(PdfHabilitacion, self).get_context_data(
            pagesize="A4",
            habilitacion=habilitacion,
            title="Solicitud de Habilitacion"
        )


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
