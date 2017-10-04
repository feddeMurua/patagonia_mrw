# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from easy_pdf.views import PDFTemplateView
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .filters import *
from .models import *
from personas import forms as f
from django.views.generic.detail import DetailView
from parte_diario_caja import forms as pd_f
from desarrollo_patagonia.utils import *


'''
ANALISIS
'''


@login_required(login_url='login')
def lista_analisis(request):
    listado_analisis = Analisis.objects.all()
    filtro_analisis = AnalisisListFilter(request.GET, queryset=listado_analisis)
    return render(request, 'analisis/analisis_list.html', {'filter': filtro_analisis})


@login_required(login_url='login')
def alta_analisis(request):
    if request.method == 'POST':
        form = AltaAnalisisForm(request.POST)
        formset = AltaPorcinoFormSet(request.POST)
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Analisis de Triquinosis')
        if form.is_valid() & formset.is_valid() & mov_diario_form.is_valid() & detalle_mov_diario_form.is_valid():
            analisis = form.save()
            porcinos = []
            for porcino_form in formset:
                porcino = porcino_form.save(commit=False)
                if porcino.precinto is not None and porcino.categoria_porcino != '':
                    porcino.analisis = analisis
                    porcinos.append(porcino)
            for porcino in porcinos:
                porcino.save()
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " - " + str(analisis.id)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip,
                                               analisis.interesado)
            detalle_mov_diario.save()
            log_crear(request.user.id, analisis, 'Analisis de Triquinosis')
            return redirect('analisis:lista_analisis')
    else:
        form = AltaAnalisisForm()
        formset = AltaPorcinoFormSet()
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Analisis de Triquinosis')
    return render(request, 'analisis/analisis_form.html', {"form": form, "formset": formset, 'can_delete': True,
                                                           'mov_diario_form': mov_diario_form,
                                                           'detalle_mov_diario_form': detalle_mov_diario_form
                                                           })


@login_required(login_url='login')
def baja_analisis(request, pk):
    analisis = Analisis.objects.get(pk=pk)
    log_eliminar(request.user.id, analisis, 'Analisis de Triquinosis')
    analisis.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_analisis(request, pk):
    analisis = Analisis.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionAnalisisForm(request.POST, instance=analisis)
        formset = ModificacionPorcinoFormSet(request.POST)
        if form.is_valid() & formset.is_valid():
            analisis = form.save()
            for porcino_form in formset:
                porcino = porcino_form.save(commit=False)
                porcino.analisis = analisis
                porcino.save()
            log_modificar(request.user.id, analisis, 'Analisis de Triquinosis')
            return redirect('analisis:lista_analisis')
    else:
        form = ModificacionAnalisisForm(instance=analisis)
        formset = ModificacionPorcinoFormSet(queryset=Porcino.objects.filter(analisis__pk=pk))
    return render(request, 'analisis/analisis_form.html', {'form': form, 'formset': formset, 'can_delete': False,
                                                           'modificacion': True})


@login_required(login_url='login')
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
    return render(request, 'criadero/solicitud_list.html', {'filter': filtro_solicitudes})


@login_required(login_url='login')
def alta_solicitud(request):
    if request.method == 'POST':
        solicitud_form = SolicitudForm(request.POST)
        domicilio_form = f.DomicilioRuralForm(request.POST)
        if solicitud_form.is_valid() & domicilio_form.is_valid():
            solicitud = solicitud_form.save(commit=False)
            solicitud.domicilio_criadero = domicilio_form.save()
            solicitud.save()
            log_crear(request.user.id, solicitud, 'Solicitud de Habilitacion')
            return redirect('criadero:lista_solicitudes')
    else:
        solicitud_form = SolicitudForm
        domicilio_form = f.DomicilioRuralForm
        return render(request, "criadero/solicitud_form.html", {'solicitud_form': solicitud_form,
                                                                'domicilio_form': domicilio_form})


@login_required(login_url='login')
def baja_solicitud(request, pk):
    solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
    log_eliminar(request.user.id, solicitud, 'Solicitud de Habilitacion')
    solicitud.delete()
    return HttpResponse()


@login_required(login_url='login')
def detalles_solicitud(request, pk):
    solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
    aplazos = AplazoSolicitud.objects.filter(solicitud__pk=pk)
    disposicion = DisposicionCriaderoCerdos.objects.filter(solicitud__pk=pk).first()
    return render(request, "criadero/solicitud_detail.html", {'solicitud': solicitud, 'aplazos': aplazos,
                                                              'disposicion': disposicion})


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
            log_modificar(request.user.id, solicitud, 'Solicitud de Habilitacion')
            return redirect('criadero:lista_solicitudes')
    else:
        form = AplazoSolicitudForm
        return render(request, 'criadero/solicitud_aplazo.html', {"form": form, 'modificacion': True})


class PdfSolicitud(LoginRequiredMixin, PDFTemplateView):
    template_name = 'criadero/solicitud_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
        return super(PdfSolicitud, self).get_context_data(
            pagesize="A4",
            solicitud=solicitud,
            title="Solicitud de Habilitacion"
        )


@login_required(login_url='login')
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
            log_crear(request.user.id, disposicion, 'Disposicion de Habilitacion')
            return redirect('criadero:lista_solicitudes')
    else:
        form = DisposicionForm
        return render(request, 'criadero/disposicion_form.html', {"form": form})


'''
ESTERILIZACION
'''


@login_required(login_url='login')
def lista_esterilizaciones(request):
    listado_esterilizaciones = Esterilizacion.objects.all()
    filtro_esterilizaciones = EsterilizacionListFilter(request.GET, queryset=listado_esterilizaciones)
    return render(request, 'esterilizacion/esterilizacion_list.html', {'filter': filtro_esterilizaciones})


class PdfConsentimiento(LoginRequiredMixin, PDFTemplateView):
    template_name = 'esterilizacion/consentimiento_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

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


@login_required(login_url='login')
def alta_esterilizacion(request):
    if request.method == 'POST':
        turno_form = TurnoForm(request.POST)
        patente_form = ListaPatentesForm(request.POST)
        if turno_form.is_valid() and patente_form.is_valid():
            patente = patente_form.cleaned_data['patente']
            esterilizacion = Esterilizacion(turno=turno_form.cleaned_data['turno'], interesado=patente.persona,
                                            mascota=patente.mascota)
            esterilizacion.save()
            log_crear(request.user.id, esterilizacion, 'Esterilizacion de Animal Patentado')
            return redirect('esterilizacion:lista_esterilizaciones')
    else:
        turno_form = TurnoForm
        patente_form = ListaPatentesForm
        return render(request, 'esterilizacion/esterilizacion_turno.html', {'turno_form': turno_form,
                                                                            'patente_form': patente_form})


@login_required(login_url='login')
def alta_esterilizacion_nopatentado(request):
    if request.method == 'POST':
        interesado_form = f.ListaPersonasGenericasForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        turno_form = TurnoForm(request.POST)
        if interesado_form.is_valid() and mascota_form.is_valid() and turno_form.is_valid():
            esterilizacion = Esterilizacion(interesado=interesado_form.cleaned_data['persona'],
                                            mascota=mascota_form.save(), turno=turno_form.cleaned_data['turno'])
            esterilizacion.save()
            log_crear(request.user.id, esterilizacion, 'Esterilizacion de Animal no Patentado')
            return redirect('esterilizacion:lista_esterilizaciones')
    else:
        interesado_form = f.ListaPersonasGenericasForm
        mascota_form = MascotaForm
        turno_form = TurnoForm
        return render(request, 'esterilizacion/esterilizacion_form.html', {'interesado_form': interesado_form,
                                                                           'mascota_form': mascota_form,
                                                                           'turno_form': turno_form})


'''
PATENTES
'''


@login_required(login_url='login')
def lista_patente(request):
    lista_patentes = Patente.objects.all()
    filtro_patentes = PatenteListFilter(request.GET, queryset=lista_patentes)
    return render(request, 'patente/patente_list.html', {'filter': filtro_patentes})


@login_required(login_url='login')
def retiro_garrapaticida(request, pk):
    patente = Patente.objects.get(pk=pk)
    if patente.fecha_garrapaticida and (now().date() - patente.fecha_garrapaticida).days <= 7:
        return HttpResponse("Aun no han pasado 7 dias desde el último retiro")
    else:
        patente.fecha_garrapaticida = datetime.now()
        patente.save()
        log_modificar(request.user.id, patente, 'Entrega de Garrapaticida')
        return HttpResponse("El retiro de garrapaticida se registro correctamente")


@login_required(login_url='login')
def retiro_antiparasitario(request, pk):
    patente = Patente.objects.get(pk=pk)
    if patente.fecha_antiparasitario and ((now().date() - patente.fecha_antiparasitario).days / 30) <= 6:
        return HttpResponse("Aun no han pasado 6 meses desde el último retiro")
    else:
        patente.fecha_antiparasitario = datetime.now()
        patente.save()
        log_modificar(request.user.id, patente, 'Entrega de Antiparasitario')
        return HttpResponse("El retiro de antiparasitario se registro correctamente")


@login_required(login_url='login')
def alta_patente(request):
    if request.method == 'POST':
        patente_form = PatenteForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(request.POST, tipo='Patentamiento')
        mov_diario_form = pd_f.MovimientoDiarioForm(request.POST)
        if patente_form.is_valid() & mascota_form.is_valid() & detalle_mov_diario_form.is_valid() & \
                mov_diario_form.is_valid():
            patente = patente_form.save(commit=False)
            mascota = mascota_form.save()
            patente.mascota = mascota
            patente.save()
            # Se crea el detalle del movimiento
            detalle_mov_diario = detalle_mov_diario_form.save(commit=False)
            servicio = detalle_mov_diario.servicio
            descrip = str(servicio) + " - Chapa: " + str(mascota.id)
            detalle_mov_diario.agregar_detalle(mov_diario_form.save(), servicio, descrip,
                                               patente.persona)
            detalle_mov_diario.save()
            log_crear(request.user.id, patente, 'Patente')
            return redirect('patentes:lista_patentes')
    else:
        patente_form = PatenteForm
        mascota_form = MascotaForm
        mov_diario_form = pd_f.MovimientoDiarioForm
        detalle_mov_diario_form = pd_f.DetalleMovimientoDiarioForm(tipo='Patentamiento')
        return render(request, "patente/patente_form.html", {'patente_form': patente_form, 'mascota_form': mascota_form,
                                                             'mov_diario_form': mov_diario_form,
                                                             'detalle_mov_diario_form': detalle_mov_diario_form})


class PdfCarnet(LoginRequiredMixin, PDFTemplateView):
    template_name = 'patente/carnet_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        patente = Patente.objects.get(pk=pk)
        return super(PdfCarnet, self).get_context_data(
            pagesize="A4",
            patente=patente,
            title="Impresion de Carnet"
        )


@login_required(login_url='login')
def baja_patente(request, pk):
    patente = Patente.objects.get(pk=pk)
    log_eliminar(request.user.id, patente, 'Patente')
    patente.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_patente(request, pk):
    patente = Patente.objects.get(pk=pk)
    if request.method == 'POST':
        patente_form = ModificacionPatenteForm(request.POST, instance=patente)
        if patente_form.is_valid():
            log_crear(request.user.id, patente_form.save(), 'Patente')
            return redirect('patentes:lista_patentes')
    else:
        patente_form = ModificacionPatenteForm(instance=patente)
    return render(request, 'patente/patente_form.html', {'patente_form': patente_form, 'modificacion': True})


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
    listado_controles = ControlAntirrabico.objects.all()
    filtro_controles = ControlListFilter(request.GET, queryset=listado_controles)
    return render(request, 'control/control_list.html', {'filter': filtro_controles})


@login_required(login_url='login')
def alta_control(request):
    if request.method == 'POST':
        control_form = ControlAntirrabicoForm(request.POST)
        if control_form.is_valid():
            log_crear(request.user.id, control_form.save(), 'Control Antirrabico')
            return redirect('controles:lista_controles')
    else:
        form = ControlAntirrabicoForm()
        return render(request, 'control/control_form.html', {"form": form})


@login_required(login_url='login')
def baja_control(request, pk):
    control = ControlAntirrabico.objects.get(pk=pk)
    log_eliminar(request.user.id, control, 'Control Antirrabico')
    control.delete()
    return HttpResponse()


class PdfInfraccion(LoginRequiredMixin, PDFTemplateView):
    template_name = 'control/infraccion_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

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


@login_required(login_url='login')
def alta_visita(request, pk_control):
    if request.method == 'POST':
        visita_form = VisitaForm(request.POST)
        if visita_form.is_valid():
            visita = visita_form.save(commit=False)
            visita.control = ControlAntirrabico.objects.get(pk=pk_control)
            visita.save()
            log_crear(request.user.id, visita, 'Visita de Control')
            return HttpResponseRedirect(reverse('controles:lista_visitas', args=pk_control))
    else:
        form = VisitaForm
        return render(request, 'control/visita_form.html', {'form': form, 'pk_control': pk_control})


@login_required(login_url='login')
def baja_visita(request, pk):
    visita = Visita.objects.get(pk=pk)
    log_crear(request.user.id, visita, 'Visita de Control')
    visita.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_visita(request, pk, pk_control):
    visita = Visita.objects.get(pk=pk)
    if request.method == 'POST':
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Visita de Control')
            return HttpResponseRedirect(reverse('controles:lista_visitas', args=pk_control))
    else:
        form = VisitaForm(instance=visita)
        return render(request, 'control/visita_form.html', {'form': form, 'pk_control': pk_control})


'''
RETIRO/ENTREGA ANIMALES
'''


@login_required(login_url='login')
def lista_retiro_entrega(request):
    listado_retiro_entrega = RetiroEntregaAnimal.objects.all()
    filtro_retiro_entrega = RetiroEntregaListFilter(request.GET, queryset=listado_retiro_entrega)
    return render(request, 'retiroEntrega/retiroEntrega_list.html', {'filter': filtro_retiro_entrega})


@login_required(login_url='login')
def alta_tramite(request):
    if 'tramite' in request.session:
        del request.session['tramite']
    if request.method == 'POST':
        retiro_entrega_form = RetiroEntregaForm(request.POST)
        if retiro_entrega_form.is_valid():
            retiro_entrega = retiro_entrega_form.save(commit=False)
            request.session['tramite'] = retiro_entrega.to_json()
            if retiro_entrega.patentado:
                return redirect('retiros_entregas:nuevo_tramite_patentado')
            else:
                return redirect('retiros_entregas:nuevo_tramite_nopatentado')
    else:
        form = RetiroEntregaForm
        return render(request, 'retiroEntrega/retiroEntrega_tramite.html', {'form': form})


@login_required(login_url='login')
def alta_tramite_patentado(request):
    if request.method == 'POST':
        tramite = request.session['tramite']
        patente_form = ListaPatentesForm(request.POST)
        if patente_form.is_valid():
            patente = patente_form.cleaned_data['patente']
            retiro_entrega = RetiroEntregaAnimal(tramite=tramite['tramite'], observaciones=tramite['observaciones'],
                                                 patentado=tramite['patentado'], interesado=patente.persona,
                                                 mascota=patente.mascota)
            if retiro_entrega.tramite == 'RETIRO':
                retiro_entrega.mascota.baja = True
                retiro_entrega.mascota.save()
            retiro_entrega.save()
            log_crear(request.user.id, retiro_entrega, 'Retiro/Entrega de Animal Patentado')
            patente.delete()
            return redirect('retiros_entregas:lista_retiro_entrega')
    else:
        form = ListaPatentesForm
        return render(request, 'retiroEntrega/retiroEntrega_patentado.html', {'form': form})


@login_required(login_url='login')
def alta_tramite_nopatentado(request):
    if request.method == 'POST':
        interesado_form = f.ListaPersonasGenericasForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        if interesado_form.is_valid() and mascota_form.is_valid():
            mascota = mascota_form.save()
            tramite = request.session['tramite']
            retiro_entrega = RetiroEntregaAnimal(tramite=tramite['tramite'], observaciones=tramite['observaciones'],
                                                 patentado=tramite['patentado'], mascota=mascota,
                                                 interesado=interesado_form.cleaned_data['persona'])
            if retiro_entrega.tramite == 'RETIRO':
                mascota.baja = True
                mascota.save()
            log_crear(request.user.id, retiro_entrega, 'Nuevo Retiro/Entrega de Animal no Patentado')
            return redirect('retiros_entregas:lista_retiro_entrega')
    else:
        interesado_form = f.ListaPersonasGenericasForm
        mascota_form = MascotaForm
        return render(request, 'retiroEntrega/retiroEntrega_noPatentado.html', {'interesado_form': interesado_form,
                                                                                'mascota_form': mascota_form})
