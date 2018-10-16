# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from easy_pdf.views import PDFTemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from .models import *
from personas import forms as f
from django.views.generic import DetailView
from parte_diario_caja import forms as pd_f
from parte_diario_caja import views as pd_v
from desarrollo_patagonia.utils import *
from django.utils import timezone
from dateutil.relativedelta import *
from desarrollo_patagonia import forms as dp_f
import json
import collections
import numpy as np


'''
ANALISIS
'''


@login_required(login_url='login')
def lista_analisis(request):
    return render(request, 'analisis/analisis_list.html', {'listado': Analisis.objects.all()})


@login_required(login_url='login')
def alta_analisis(request):
    porcino_form = PorcinoForm
    if request.method == 'POST':
        form = AltaAnalisisForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if form.is_valid():
            analisis = form.save()
            alta_porcinos(request, analisis)
            servicio = 'Analisis de triquinosis'
            if request.POST['optradio'] == 'previa':
                if detalle_mov_form.is_valid():
                    pd_v.movimiento_previo(request, detalle_mov_form, servicio, analisis, servicio)
                    return redirect('analisis:lista_analisis')
            else:
                if mov_form.is_valid():
                    pd_v.nuevo_movimiento(request, mov_form, servicio, analisis, servicio)
                    return redirect('analisis:lista_analisis')
    else:
        if 'porcinos' in request.session:
            del request.session['porcinos']
        request.session['porcinos'] = []
        form = AltaAnalisisForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'analisis/analisis_form.html', {'form': form, 'porcino_form': porcino_form,
                                                           'mov_form': mov_form, 'detalle_mov_form': detalle_mov_form})


def existe_porcino(request, porcino):
    for item in request.session['porcinos']:
        if item['precinto'] == porcino.precinto:
            return True
    return False


@login_required(login_url='login')
def agregar_porcino(request):
    form = PorcinoForm(request.POST)
    success = True
    if form.is_valid():
        porcino = form.save(commit=False)
        if existe_porcino(request, porcino):
            success = False
        else:
            request.session['porcinos'].append(porcino.to_json())
            request.session.modified = True
    return JsonResponse({'success': success, 'porcinos': request.session['porcinos']})


@login_required(login_url='login')
def eliminar_porcino(request, precinto):
    porcinos = request.session['porcinos']
    porcinos[:] = [p for p in porcinos if p['precinto'] != int(precinto)]
    request.session['porcinos'] = porcinos
    return JsonResponse({'porcinos': request.session['porcinos']})


def alta_porcinos(request, analisis):
    for porcino in request.session['porcinos']:
        item = Porcino(precinto=porcino['precinto'], categoria_porcino=porcino['categoria_porcino'], analisis=analisis)
        item.save()
    return HttpResponse()


def actualizacion_porcinos(request, analisis):
    dbporcinos = Porcino.objects.filter(analisis=analisis)
    dbprecintos = dbporcinos.values_list('precinto', flat=True)
    sporcinos = request.session['porcinos']
    sprecintos = []
    for porcino in sporcinos:
        sprecintos.append(porcino['precinto'])
    for porcino in sporcinos:
        if porcino['precinto'] not in dbprecintos:
            item = Porcino(precinto=porcino['precinto'], categoria_porcino=porcino['categoria_porcino'],
                           analisis=analisis)
            item.save()
    for porcino in dbporcinos:
        if porcino.precinto not in sprecintos:
            porcino.delete()
    return HttpResponse()


def porcinostoSession(request, analisis):
    request.session['porcinos'] = []
    porcinos = Porcino.objects.filter(analisis=analisis)
    for porcino in porcinos:
        request.session['porcinos'].append(porcino.to_json())
        request.session.modified = True
    return HttpResponse()


@login_required(login_url='login')
def modificacion_analisis(request, pk):
    porcino_form = PorcinoForm
    analisis = Analisis.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionAnalisisForm(request.POST, instance=analisis)
        if form.is_valid():
            analisis = form.save()
            actualizacion_porcinos(request, analisis)
            log_modificar(request.user.id, analisis, 'Analisis de Triquinosis')
            return redirect('analisis:lista_analisis')
    else:
        if 'porcinos' in request.session:
            del request.session['porcinos']
        porcinostoSession(request, analisis)
        form = ModificacionAnalisisForm(instance=analisis)
    return render(request, 'analisis/analisis_form.html', {'form': form, 'porcinos': request.session['porcinos'],
                                                           'porcino_form': porcino_form, 'modificacion': True})


@login_required(login_url='login')
def baja_analisis(request, pk):
    analisis = Analisis.objects.get(pk=pk)
    log_eliminar(request.user.id, analisis, 'Analisis de Triquinosis')
    analisis.delete()
    return HttpResponse()


@login_required(login_url='login')
def resultado_analisis(request, pk):
    analisis = Analisis.objects.get(pk=pk)
    if request.method == 'POST':
        form = ResultadoAnalisisForm(request.POST, instance=analisis)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Analisis de Triquinosis')
            return redirect('analisis:lista_analisis')
    else:
        form = ResultadoAnalisisForm(instance=analisis)
    return render(request, 'analisis/analisis_form.html', {'form': form, 'modificacion': True})


@login_required(login_url='login')
def detalle_analisis(request, pk):
    analisis = Analisis.objects.get(pk=pk)
    porcinos = Porcino.objects.filter(analisis__pk=pk)
    return render(request, 'analisis/analisis_detail.html', {'analisis': analisis, 'porcinos': porcinos})


class PdfAnalisis(LoginRequiredMixin, PDFTemplateView):
    template_name = 'analisis/analisis_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        analisis = Analisis.objects.get(pk=pk)
        return super(PdfAnalisis, self).get_context_data(
            analisis=analisis,
            porcinos=Porcino.objects.filter(analisis=analisis),
            title='Analisis N°'
        )


'''
SOLICITUD/HABILITACION CRIADERO DE CERDOS
'''


@login_required(login_url='login')
def lista_solicitudes(request):
    return render(request, 'criadero/solicitud_list.html', {'listado': SolicitudCriaderoCerdos.objects.all()})


@login_required(login_url='login')
def alta_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        domicilio_form = f.DomicilioRuralForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.domicilio_criadero = domicilio_form.save()
            solicitud.save()
            log_crear(request.user.id, solicitud, 'Solicitud de Habilitacion')
            return redirect('criadero:lista_solicitudes')
    else:
        form = SolicitudForm
        domicilio_form = f.DomicilioRuralForm
    return render(request, "criadero/solicitud_form.html", {'form': form, 'domicilio_form': domicilio_form})


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
        form = AplazoSolicitudForm(request.POST)
        if form.is_valid():
            aplazo = form.save(commit=False)
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
        return super(PdfSolicitud, self).get_context_data(
            solicitud=SolicitudCriaderoCerdos.objects.get(pk=pk),
            title='Solicitud N°'
        )


@login_required(login_url='login')
def alta_disposicion(request, pk):
    if request.method == 'POST':
        form = DisposicionForm(request.POST)
        if form.is_valid():
            disposicion = form.save(commit=False)
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
    return render(request, 'esterilizacion/esterilizacion_list.html', {'listado': Esterilizacion.objects.all()})


class PdfConsentimiento(LoginRequiredMixin, PDFTemplateView):
    template_name = 'esterilizacion/consentimiento_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        esterilizacion = Esterilizacion.objects.get(pk=pk)
        tiempo_edad = None
        edad_mascota = None
        if esterilizacion.mascota.nacimiento_fecha:
            edad_mascota = (timezone.now().date() - esterilizacion.mascota.nacimiento_fecha).days / 30
            tiempo_edad = 'MESES'
            if 11 < edad_mascota < 24:
                edad_mascota = 1
                tiempo_edad = 'AÑO'
            elif edad_mascota > 23:
                edad_mascota = int(edad_mascota/12)
                tiempo_edad = 'AÑOS'
        return super(PdfConsentimiento, self).get_context_data(
            esterilizacion=esterilizacion,
            tiempo_edad=tiempo_edad,
            edad_mascota=edad_mascota,
            title='Esterilizacion N°'
        )


@login_required(login_url='login')
def alta_esterilizacion(request):
    if request.method == 'POST':
        form = ListaPatentesEsterilizacionForm(request.POST)
        esterilizacion_form = EsterilizacionPatenteForm(request.POST)
        if form.is_valid() & esterilizacion_form.is_valid():
            esterilizacion = esterilizacion_form.save(commit=False)
            patente = form.cleaned_data['patente']
            esterilizacion.interesado = patente.persona
            esterilizacion.mascota = patente.mascota
            esterilizacion.save()
            log_crear(request.user.id, esterilizacion, 'Turno para Esterilizacion de Animal Patentado')
            return redirect('esterilizacion:lista_esterilizaciones')
    else:
        form = ListaPatentesEsterilizacionForm
        esterilizacion_form = EsterilizacionPatenteForm
    return render(request, 'esterilizacion/esterilizacion_patentada.html', {'form': form,
                                                                        'esterilizacion_form': esterilizacion_form})


@login_required(login_url='login')
def alta_esterilizacion_nopatentado(request):
    if request.method == 'POST':
        form = EsterilizacionNuevoForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        if form.is_valid() & mascota_form.is_valid():
            esterilizacion = form.save(commit=False)
            esterilizacion.mascota = mascota_form.save()
            esterilizacion.save()
            log_crear(request.user.id, esterilizacion, 'Turno para Esterilizacion de Animal no Patentado')
            return redirect('esterilizacion:lista_esterilizaciones')
    else:
        form = EsterilizacionNuevoForm
        mascota_form = MascotaForm
    return render(request, 'esterilizacion/esterilizacion_no_patentada.html', {'form': form, 'mascota_form': mascota_form})


@login_required(login_url='login')
def baja_esterilizacion(request, pk):
    esterilizacion = Esterilizacion.objects.get(pk=pk)
    log_eliminar(request.user.id, esterilizacion, 'Turno para Esterilizacion')
    esterilizacion.delete()
    return HttpResponse()


@login_required(login_url='login')
def confirmar_esterilizacion(request, pk):
    mascota = Esterilizacion.objects.get(pk=pk).mascota
    mascota.esterilizado = True
    mascota.save()
    log_crear(request.user.id, mascota, 'Confirmacion de Esterilizacion')
    return HttpResponse()


'''
PATENTES
'''


@login_required(login_url='login')
def lista_patente(request):
    return render(request, 'patente/patente_list.html', {'listado': Patente.objects.all(),
                                                         'fecha_hoy': timezone.now().date()})


@login_required(login_url='login')
def retiro_garrapaticida(request, pk):
    patente = Patente.objects.get(pk=pk)
    if patente.fecha_garrapaticida and (timezone.now().date() - patente.fecha_garrapaticida).days <= 7:
        return JsonResponse({'msg': "Aun no han pasado 7 dias desde el último retiro", 'error': True})
    else:
        patente.fecha_garrapaticida = timezone.now()
        patente.save()
        log_crear(request.user.id, patente, 'Entrega de Garrapaticida')
        return JsonResponse({'msg': "El retiro de garrapaticida se registro correctamente", 'error': False})


@login_required(login_url='login')
def retiro_antiparasitario(request, pk):
    patente = Patente.objects.get(pk=pk)
    if patente.fecha_antiparasitario and ((timezone.now().date() - patente.fecha_antiparasitario).days / 30) <= 6:
        return JsonResponse({'msg': "Aun no han pasado 6 meses desde el último retiro", 'error': True})
    else:
        patente.fecha_antiparasitario = timezone.now()
        patente.save()
        log_crear(request.user.id, patente, 'Entrega de Antiparasitario')
        return JsonResponse({'msg': "El retiro de antiparasitario se registro correctamente", 'error': False})


@login_required(login_url='login')
def alta_patente(request):
    if request.method == 'POST':
        form = PatenteForm
        mascota_form = MascotaForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if mascota_form.is_valid():
            mascota = mascota_form.save(commit=False)
            form = PatenteForm(request.POST, categoria=mascota.categoria_mascota)
            if form.is_valid():
                mascota.esterilizado = False
                mascota.save()
                patente = form.save(commit=False)
                patente.mascota = mascota
                patente.fecha_vencimiento = timezone.now().date() + relativedelta(years=1)
                if request.POST['optradio'] == 'previa':
                    if detalle_mov_form.is_valid():
                        patente.save()
                        pd_v.movimiento_previo(request, detalle_mov_form, "Registro/patente anual", patente, 'Patente')
                        return redirect('patentes:lista_patentes')
                else:
                    if mov_form.is_valid():
                        patente.save()
                        pd_v.nuevo_movimiento(request, mov_form, "Registro/patente anual", patente, 'Patente')
                        return redirect('patentes:lista_patentes')
    else:
        form = PatenteForm
        mascota_form = MascotaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, "patente/patente_form.html", {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                         'mascota_form': mascota_form, 'mov_form': mov_form})


class PdfCarnet(LoginRequiredMixin, PDFTemplateView):
    template_name = 'patente/carnet_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        patente = Patente.objects.get(pk=pk)
        return super(PdfCarnet, self).get_context_data(
            patente=patente,
            title='Patente N°: ' + str(patente.nro_patente)
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
        form = ModificacionPatenteForm(request.POST, instance=patente)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Patente')
            return redirect('patentes:lista_patentes')
    else:
        form = ModificacionPatenteForm(instance=patente)
    return render(request, 'patente/patente_form.html', {'form': form, 'modificacion': True})


@login_required(login_url='login')
def reno_dup_patente(request, pk):
    patente = Patente.objects.get(pk=pk)
    if request.method == 'POST':
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if request.POST['radio'] == 'renovacion':
            patente.fecha_vencimiento = timezone.now().date() + relativedelta(years=1)
            patente.save()
            servicio = "Renovacion de patente"
        else:
            servicio = "Duplicado de patente"
        if request.POST['optradio'] == 'previa':
            if detalle_mov_form.is_valid():
                pd_v.movimiento_previo(request, detalle_mov_form, servicio, patente, servicio)
                return redirect('patentes:lista_patentes')
        else:
            if mov_form.is_valid():
                pd_v.nuevo_movimiento(request, mov_form, servicio, patente, servicio)
                return redirect('patentes:lista_patentes')
    else:
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'patente/patente_reno_dup.html', {'detalle_mov_form': detalle_mov_form, 'patente': patente,
                                                             'fecha_hoy': timezone.now().date(), 'mov_form': mov_form})


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
    return render(request, 'control/control_list.html', {'listado': ControlAntirrabico.objects.all()})


@login_required(login_url='login')
def alta_control(request):
    if request.method == 'POST':
        form = ControlAntirrabicoForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if form.is_valid():
            servicio = 'Control antirrabico'
            if request.POST['optradio'] == 'previa':
                if detalle_mov_form.is_valid():
                    control = form.save()
                    pd_v.movimiento_previo(request, detalle_mov_form, servicio, control, servicio)
                    return redirect('controles:lista_controles')
            else:
                if mov_form.is_valid():
                    control = form.save()
                    pd_v.nuevo_movimiento(request, mov_form, servicio, control, servicio)
                    return redirect('controles:lista_controles')
    else:
        form = ControlAntirrabicoForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'control/control_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                         'mov_form': mov_form})


@login_required(login_url='login')
def baja_control(request, pk):
    control = ControlAntirrabico.objects.get(pk=pk)
    log_eliminar(request.user.id, control, 'Control Antirrabico')
    control.delete()
    return HttpResponse()


@login_required(login_url='login')
def lista_visitas_control(request, pk_control):
    return render(request, 'control/visita_list.html', {'pk_control': pk_control,
                                                        'listado': Visita.objects.filter(control__pk=pk_control)})


@login_required(login_url='login')
def alta_visita(request, pk_control):
    control = ControlAntirrabico.objects.get(pk=pk_control)
    if request.method == 'POST':
        form = VisitaForm(request.POST, control=control)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.control = control
            visita.save()
            log_crear(request.user.id, visita, 'Visita de Control')
            return HttpResponseRedirect(reverse('controles:lista_visitas', args=[pk_control]))
    else:
        form = VisitaForm
    return render(request, 'control/visita_form.html', {'form': form, 'pk_control': pk_control})


@login_required(login_url='login')
def baja_visita(request, pk):
    visita = Visita.objects.get(pk=pk)
    log_eliminar(request.user.id, visita, 'Visita de Control')
    visita.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_visita(request, pk, pk_control):
    visita = Visita.objects.get(pk=pk)
    if request.method == 'POST':
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Visita de Control')
            return HttpResponseRedirect(reverse('controles:lista_visitas', args=[pk_control]))
    else:
        form = VisitaForm(instance=visita)
    return render(request, 'control/visita_form.html', {'form': form, 'pk_control': pk_control})


'''
SACRIFICIO/ENTREGA DE ANIMALES
'''


@login_required(login_url='login')
def lista_retiro_entrega(request):
    return render(request, 'retiroEntrega/retiroEntrega_list.html', {'listado': RetiroEntregaAnimal.objects.all()})


@login_required(login_url='login')
def alta_tramite(request):
    if request.method == 'POST':
        form = RetiroEntregaForm(request.POST)
        patentes_form = ListaPatentesForm(request.POST)
        personas_form = f.ListaPersonasGenericasForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        if form.is_valid():
            retiro_entrega = form.save(commit=False)
            if 'patentado' in request.POST and patentes_form.is_valid():
                patente = patentes_form.cleaned_data['patente']
                retiro_entrega.interesado = patente.persona
                retiro_entrega.mascota = patente.mascota
                retiro_entrega.patente = patente.nro_patente
                if retiro_entrega.tramite == 'SACRIFICIO':
                    retiro_entrega.mascota.baja = True
                    retiro_entrega.mascota.save()
                retiro_entrega.save()
                log_crear(request.user.id, retiro_entrega, 'Sacrificio/Entrega de Animal Patentado')
                patente.delete()
                return redirect('sacrificios_entregas:lista_retiro_entrega')
            else:
                mascota = mascota_form.save()
                retiro_entrega.mascota = mascota
                retiro_entrega.interesado = form.cleaned_data['persona']
                if retiro_entrega.tramite == 'SACRIFICIO':
                    mascota.baja = True
                    mascota.save()
                retiro_entrega.save()
                log_crear(request.user.id, retiro_entrega, 'Nuevo Sacrificio/Entrega de Animal no Patentado')
                return redirect('sacrificios_entregas:lista_retiro_entrega')
    else:
        form = RetiroEntregaForm
        patentes_form = ListaPatentesForm
        personas_form = f.ListaPersonasGenericasForm
        mascota_form = MascotaForm
    return render(request, 'retiroEntrega/retiroEntrega_tramite.html', {'form': form, 'patentes_form': patentes_form,
                                                                        'personas_form': personas_form,
                                                                        'mascota_form': mascota_form})


@login_required(login_url='login')
def modificacion_tramite(request, pk):
    tramite = RetiroEntregaAnimal.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionRetiroEntregaForm(request.POST, instance=tramite)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Sacrificio/Entrega de Animal')
            return redirect('sacrificios_entregas:lista_retiro_entrega')
    else:
        form = ModificacionRetiroEntregaForm(instance=tramite)
    return render(request, 'retiroEntrega/retiroEntrega_modificacion.html', {'form': form})


@login_required(login_url='login')
def estadisticas_animales(request):
    rango_form = dp_f.RangoAnioForm
    years = [timezone.now().year]
    if request.method == 'POST':
        rango_form = dp_f.RangoAnioForm(request.POST)
        if rango_form.is_valid():
            years = range(int(rango_form.cleaned_data['anio_hasta']),
                          int(rango_form.cleaned_data['anio_desde']) - 1, -1)

    # CANTIDAD DE ANALISIS
    todos_analisis = {}
    for year in years:
        todos_analisis[str(year)] = Analisis.objects.filter(fecha__year=year).count()
    ord_analisis = collections.OrderedDict(sorted(todos_analisis.items()))
    label_analisis = ord_analisis.keys()
    datos_analisis = ord_analisis.values()

    # CATEGORIAS DE ANALISIS
    analisis_categorias = to_counter(Porcino, {'analisis__fecha__year__lte': years[0],
                                               'analisis__fecha__year__gte': years[-1]}, ['categoria_porcino'])

    context = {
        'rango_form': rango_form,
        'promedio_analisis': int(np.average(datos_analisis)),
        # datos y etiquetas
        'lista_labels': json.dumps([label_analisis, analisis_categorias.keys()]),
        'lista_datos': json.dumps([{'Analisis': datos_analisis}, {'Categorias': analisis_categorias.values()}])
    }
    return render(request, "estadistica/estadisticas_analisis.html", context)


@login_required(login_url='login')
def estadisticas_mascotas(request):
    rango_form = dp_f.RangoAnioForm
    years = [timezone.now().year]
    if request.method == 'POST':
        rango_form = dp_f.RangoAnioForm(request.POST)
        if rango_form.is_valid():
            years = range(int(rango_form.cleaned_data['anio_hasta']),
                          int(rango_form.cleaned_data['anio_desde']) - 1, -1)

    # PATENTAMIENTO
    tipo_patente = to_counter(Patente, {'fecha__year__lte': years[0], 'fecha__year__gte': years[-1]},
                              ['mascota__categoria_mascota', 'mascota__sexo'])

    # ESTERILIZACION
    tipo_esterilizacion = to_counter(Esterilizacion, {'turno__year__lte': years[0], 'turno__year__gte': years[-1]},
                                     ['mascota__categoria_mascota', 'mascota__sexo'])

    # SACRIFICIO Y ENTREGA DE ANIMALES
    tramites = to_counter(RetiroEntregaAnimal, {'fecha__year__lte': years[0], 'fecha__year__gte': years[-1]},
                          ['tramite', 'mascota__categoria_mascota', 'mascota__sexo'])

    context = {
        'rango_form': rango_form,
        'lista_labels': json.dumps([tipo_patente.keys(), tipo_esterilizacion.keys(), tramites.keys()]),
        'lista_datos': json.dumps([{'Tipo Patente': tipo_patente.values()},
                                   {'Tipo Esterilizacion': tipo_esterilizacion.values()},
                                   {'Tramites': tramites.values()}])
    }
    return render(request, "estadistica/estadisticas_mascotas.html", context)
