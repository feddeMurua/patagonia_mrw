# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from easy_pdf.views import PDFTemplateView
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .filters import *
from .models import *
from personas import models as m
from personas import forms as f
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)


@login_required(login_url='login')
def get_mascotas(request, pk_interesado):
    patentes = Patente.objects.filter(persona__pk=pk_interesado)
    mascotas = []
    for patente in patentes:
        mascotas.append({'text': patente.mascota.nombre, 'value': patente.mascota.nombre})
    return HttpResponse(mascotas)


'''
ANALISIS
'''


@login_required(login_url='login')
def lista_analisis(request):
    lista_analisis = Analisis.objects.all()
    filtro_analisis = AnalisisListFilter(request.GET, queryset=lista_analisis)
    fecha_hoy = now
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


def alta_solicitud(request):
    if request.method == 'POST':
        solicitud_form = SolicitudForm(request.POST)
        domicilio_form = f.DomicilioRuralForm(request.POST)
        if solicitud_form.is_valid() & domicilio_form.is_valid():
            solicitud = solicitud_form.save(commit=False)
            domicilio = domicilio_form.save(commit=False)
            domicilio.save()
            solicitud.domicilio_criadero = domicilio
            solicitud.save()
            return redirect('solicitud:lista_solicitudes')
    else:
        solicitud_form = SolicitudForm
        domicilio_form = f.DomicilioRuralForm
        return render(request, "solicitud/solicitud_form.html", {'solicitud_form': solicitud_form,
                                                             'domicilio_form': domicilio_form})


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
    disposicion = DisposicionCriaderoCerdos.objects.filter(solicitud__pk=pk).first()
    return render(request, "solicitud/solicitud_detail.html", {'solicitud': solicitud, 'aplazos': aplazos,
                                                               'disposicion': disposicion})


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
            aplazo.save()
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


class PdfConsentimiento(PDFTemplateView):
    template_name = 'esterilizacion/consentimiento_pdf.html'

    def get_context_data(self, pk_esterilizacion):
        esterilizacion = Esterilizacion.objects.get(pk=pk_esterilizacion)
        edad_mascota = (datetime.now().date() - esterilizacion.mascota.fecha_nacimiento).days / 30
        tiempo_edad = 'MESES'
        if 11 < edad_mascota < 24:
            edad_mascota = 1
            tiempo_edad = 'AÑO'
        elif edad_mascota > 23:
            edad_mascota = int(edad_mascota/12)
            tiempo_edad = 'AÑOS'
        return super(PdfConsentimiento, self).get_context_data(
            pagesize="A4",
            esterilizacion=esterilizacion,
            tiempo_edad=tiempo_edad,
            edad_mascota=edad_mascota,
            title="Consentimiento de Esterilizacion"
        )


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


def retiro_garrapaticida(request, pk):
    patente = Patente.objects.get(pk=pk)
    dias_ultimo_retiro = (now().date() - patente.fecha_garrapaticida).days
    if dias_ultimo_retiro <= 7:
        return HttpResponse("Aun no han pasado 7 dias desde el último retiro")
    else:
        patente.fecha_garrapaticida = datetime.now()
        patente.save()
        return HttpResponse("Retiro confirmado")


def retiro_antiparasitario(request, pk):
    patente = Patente.objects.get(pk=pk)
    meses_ultimo_retiro = ((now().date() - patente.fecha_antiparasitario).days / 30)
    print (meses_ultimo_retiro)
    if meses_ultimo_retiro <= 6:
        return HttpResponse("Aun no han pasado 6 meses desde el último retiro")
    else:
        patente.fecha_antiparasitario = datetime.now()
        patente.save()
        return HttpResponse("Retiro confirmado")


def alta_patente(request):
    if request.method == 'POST':
        patente_form = PatenteForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        if patente_form.is_valid() & mascota_form.is_valid():
            patente = patente_form.save(commit=False)
            mascota = mascota_form.save(commit=False)
            mascota.save()
            patente.mascota = mascota
            patente.save()
            return redirect('patentes:lista_patentes')
    else:
        patente_form = PatenteForm
        mascota_form = MascotaForm
        return render(request, "patente/patente_form.html", {'patente_form': patente_form,
                                                             'mascota_form': mascota_form})





class PdfCarnet(PDFTemplateView):
    template_name = 'patente/carnet_pdf.html'

    def get_context_data(self, pk):
        patente = Patente.objects.get(pk=pk)
        return super(PdfCarnet, self).get_context_data(
            pagesize="A4",
            patente=patente,
            title="Impresion de Carnet"
        )


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


class DetallePatente(LoginRequiredMixin, DetailView):
    model = Patente
    template_name = 'patente/patente_detail.html'
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
                # ACA SE TIENE QUE VERIFICAR SI LAS PERSONAS SON IGUALES
                return redirect('controles:nuevo_control')
    else:
        form = ControlAntirrabicoForm()
        return render(request, 'control/control_form.html', {"form": form})


class PdfInfraccion(PDFTemplateView):
    template_name = 'control/infraccion_pdf.html'

    def get_context_data(self, pk_control):
        control = ControlAntirrabico.objects.get(pk=pk_control)
        return super(PdfInfraccion, self).get_context_data(
            pagesize="A4",
            control=control,
            title="Acta de Infraccion"
        )



@login_required(login_url='login')
def lista_visitas_control(request, pk_control):
    lista_visitas = Visita.objects.filter(control__pk=pk_control)
    filtro_visitas = VisitaListFilter(request.GET, queryset=lista_visitas)
    control = ControlAntirrabico.objects.get(pk=pk_control)
    dias_suceso = (now().date() - control.fecha_suceso).days
    ultima_visita = lista_visitas.last()
    apto_visita = True
    if dias_suceso > 10 or (ultima_visita and ultima_visita.fecha_visita == now().date()):
          apto_visita = False
    return render(request, 'control/visita_list.html', {'pk_control': pk_control, 'filter': filtro_visitas,
                                                        'apto_visita': apto_visita})


def alta_visita(request, pk_control):
    if request.method == 'POST':
        visita_form = VisitaForm(request.POST)
        if visita_form.is_valid():
            visita = visita_form.save(commit=False)
            visita.control = ControlAntirrabico.objects.get(pk=pk_control)
            visita.save()
            return HttpResponseRedirect(reverse('controles:lista_visitas', args=pk_control))
    else:
        form = VisitaForm
        return render(request, 'control/visita_form.html', {'form': form, 'pk_control': pk_control})


class BajaVisita(LoginRequiredMixin, DeleteView):
    model = Visita
    template_name = 'control/visita_confirm_delete.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_success_url(self):
        if 'pk_control' in self.kwargs:
            pk_control = self.kwargs['pk_control']
        return reverse('controles:lista_visitas', kwargs={'pk_control': pk_control})


class ModificacionVisita(LoginRequiredMixin, UpdateView):
    model = Visita
    template_name = 'control/visita_form.html'
    fields = ['observaciones']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_success_url(self):
        if 'pk_control' in self.kwargs:
            pk_control = self.kwargs['pk_control']
        return reverse('controles:lista_visitas', kwargs={'pk_control': pk_control})


'''
RETIRO/ENTREGA ANIMALES
'''


@login_required(login_url='login')
def lista_retiro_entrega(request):
    lista_retiro_entrega = RetiroEntregaAnimal.objects.all()
    filtro_retiro_entrega = RetiroEntregaListFilter(request.GET, queryset=lista_retiro_entrega)
    return render(request, 'retiroEntrega/retiroEntrega_list.html', {'filter': filtro_retiro_entrega})


def alta_retiro_etrega(request):
    if request.method == 'POST':
        pass
    else:
        tramite_form = TramiteForm
        mascota_patente_form = MascotaPatentadaForm
        mascota_form = MascotaForm
        patente_form = PatenteForm
        return render(request, 'retiroEntrega/retiroEntrega_form.html', {'tramite_form': tramite_form,
                                                                         'mascota_form': mascota_form,
                                                                         'patente_form': patente_form,
                                                                         'mascota_patente_form': mascota_patente_form})


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
