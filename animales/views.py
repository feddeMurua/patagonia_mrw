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
from personas import models as m
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


@login_required(login_url='login')
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
SOLICITUD/HABILITACION CRIADERO DE CERDOS
'''


@login_required(login_url='login')
def lista_solicitudes(request):
    solicitudes = SolicitudCriaderoCerdos.objects.all()
    filtro_solicitudes = SolicitudListFilter(request.GET, queryset=solicitudes)
    return render(request, 'solicitud/solicitud_list.html', {'filter': filtro_solicitudes})


class AltaSolicitud(LoginRequiredMixin, CreateView):
    model = SolicitudCriaderoCerdos
    template_name = 'solicitud/solicitud_form.html'
    success_url = reverse_lazy('solicitud:lista_solicitudes')
    form_class = SolicitudForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaSolicitud(LoginRequiredMixin, DeleteView):
    model = SolicitudCriaderoCerdos
    template_name = 'solicitud/solicitud_confirm_delete.html'
    success_url = reverse_lazy('solicitud:lista_solicitudes')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def detalles_solicitud(request, pk):
    solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
    aplazos = AplazoSolicitud.objects.filter(solicitud__pk=pk)
    return render(request, "solicitud/solicitud_detail.html", {'solicitud': solicitud,
                                                           'aplazos': aplazos})


class DetalleSolicitud(LoginRequiredMixin, DetailView):
    model = SolicitudCriaderoCerdos
    template_name = 'solicitud/solicitud_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def aplazo_solicitud(request, pk):
    if request.method == 'POST':
        aplazo_form = AplazoSolicitudForm(request.POST)
        if aplazo_form.is_valid():
            aplazo = aplazo_form.save(commit=False)
            solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
            solicitud.motivo_aplazo = aplazo.motivo_aplazo
            solicitud.estado = 'Aplazada'
            solicitud.save()
            aplazo.solicitud = solicitud
            return redirect('solicitud:lista_solicitudes')
    else:
        form = AplazoSolicitudForm
        return render(request, 'solicitud/solicitud_aplazo.html', {"form": form})


class PdfSolicitud(PDFTemplateView):
    template_name = 'solicitud/solicitud_pdf.html'

    def get_context_data(self, pk):
        solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
        return super(PdfSolicitud, self).get_context_data(
            pagesize="A4",
            solicitud=solicitud,
            title="Solicitud de Habilitacion"
        )


def alta_disposicion(request, pk):
    if request.method == 'POST':
        disposicion_form = DisposicionForm(request.POST)
        if disposicion_form.is_valid():
            disposicion = disposicion_form.save(commit=False)
            solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
            solicitud.estado = 'Aprobada'
            solicitud.save()
            disposicion.solicitud = solicitud
            disposicion.save()
            return redirect('solicitud:lista_solicitudes')
    else:
        form = DisposicionForm
        return render(request, 'disposicion/disposicion_form.html', {"form": form})


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
CONTROL ANTIRRABICO
'''


@login_required(login_url='login')
def lista_controles(request):
    lista_controles = ControlAntirrabico.objects.all()
    filtro_controles = ControlListFilter(request.GET, queryset=lista_controles)
    return render(request, 'control/control_list.html', {'filter': filtro_controles})


@login_required(login_url='login')
def alta_control(request):
    if request.method == 'POST':
        control_form = ControlAntirrabicoForm(request.POST)
        if control_form.is_valid():
            control_antirrabico = control_form.save(commit=False)
            mordido = m.PersonaFisica.objects.get(dni=control_antirrabico.mordido.dni)
            responsable = m.PersonaFisica.objects.get(dni=control_antirrabico.responsable.dni)
            if mordido.dni != responsable.dni:
                control_antirrabico.save()
                return redirect('controles:lista_controles')
            else:
                #ACA SE TIENE QUE VERIFICAR SI LAS PERSONAS SON IGUALES
                return redirect('controles:nuevo_control')
    else:
        form = ControlAntirrabicoForm()
        return render(request, 'control/control_form.html', {"form": form})


'''
RETIRO/ENTREGA ANIMALES
'''


@login_required(login_url='login')
def lista_retiro_entrega(request):
    lista_retiro_entrega = RetiroEntregaAnimal.objects.all()
    filtro_retiro_entrega = RetiroEntregaListFilter(request.GET, queryset=lista_retiro_entrega)
    return render(request, 'retiroEntrega/retiroEntrega_list.html', {'filter': filtro_retiro_entrega})


class AltaRetiroEntrega(LoginRequiredMixin, CreateView):
    model = RetiroEntregaAnimal
    template_name = 'retiroEntrega/retiroEntrega_form.html'
    success_url = reverse_lazy('retiros_entregas:lista_retiro_entrega')
    form_class = RetiroEntregaForm
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
