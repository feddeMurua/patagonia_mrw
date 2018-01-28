# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from easy_pdf.views import PDFTemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .models import *
from personas import forms as f
from django.views.generic import DetailView
from parte_diario_caja import forms as pd_f
from parte_diario_caja import models as pd_m
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
    if request.method == 'POST':
        form = AltaAnalisisForm(request.POST)
        formset = AltaPorcinoFormSet(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        servicio_form = pd_f.ListaServicios(request.POST, tipo='Analisis de Triquinosis')
        if form.is_valid() & formset.is_valid() & detalle_mov_form.is_valid() & servicio_form.is_valid():
            analisis = form.save()

            # logica formset

            for form in formset.forms:
                porcino_item = form.save(commit=False)
                porcino_item.analisis = analisis
                porcino_item.save()
            detalle_mov = detalle_mov_form.save(commit=False)
            detalle_mov.completar(servicio_form.cleaned_data['servicio'], analisis)
            log_crear(request.user.id, analisis, 'Analisis de Triquinosis')
            return redirect('analisis:lista_analisis')
    else:
        form = AltaAnalisisForm
        formset = AltaPorcinoFormSet
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        servicio_form = pd_f.ListaServicios(tipo='Analisis de Triquinosis')
    return render(request, 'analisis/analisis_form.html', {'form': form, 'formset': formset, 'can_delete': True,
                                                           'detalle_mov_form': detalle_mov_form,
                                                           'servicio_form': servicio_form})


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
        solicitud = SolicitudCriaderoCerdos.objects.get(pk=pk)
        return super(PdfSolicitud, self).get_context_data(
            pagesize="A4",
            solicitud=solicitud
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

    def get_context_data(self, pk_esterilizacion):
        esterilizacion = Esterilizacion.objects.get(pk=pk_esterilizacion)
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
            pagesize="A4",
            esterilizacion=esterilizacion,
            tiempo_edad=tiempo_edad,
            edad_mascota=edad_mascota
        )


@login_required(login_url='login')
def alta_esterilizacion(request):
    if request.method == 'POST':
        form = ListaPatentesForm(request.POST)
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
        form = ListaPatentesForm
        esterilizacion_form = EsterilizacionPatenteForm
    return render(request, 'esterilizacion/esterilizacion_turno.html', {'form': form,
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
    return render(request, 'esterilizacion/esterilizacion_form.html', {'form': form, 'mascota_form': mascota_form})


@login_required(login_url='login')
def baja_esterilizacion(request, pk):
    esterilizacion = Esterilizacion.objects.get(pk=pk)
    log_eliminar(request.user.id, esterilizacion, 'Turno para Esterilizacion')
    esterilizacion.delete()
    return HttpResponse()


'''
PATENTES
'''


@login_required(login_url='login')
def lista_patente(request):
    return render(request, 'patente/patente_list.html', {'listado': Patente.objects.all()})


@login_required(login_url='login')
def retiro_garrapaticida(request, pk):
    patente = Patente.objects.get(pk=pk)
    if patente.fecha_garrapaticida and (timezone.now().date() - patente.fecha_garrapaticida).days <= 7:
        return HttpResponse("Aun no han pasado 7 dias desde el último retiro")
    else:
        patente.fecha_garrapaticida = timezone.now()
        patente.save()
        log_modificar(request.user.id, patente, 'Entrega de Garrapaticida')
        return HttpResponse("El retiro de garrapaticida se registro correctamente")


@login_required(login_url='login')
def retiro_antiparasitario(request, pk):
    patente = Patente.objects.get(pk=pk)
    if patente.fecha_antiparasitario and ((timezone.now().date() - patente.fecha_antiparasitario).days / 30) <= 6:
        return HttpResponse("Aun no han pasado 6 meses desde el último retiro")
    else:
        patente.fecha_antiparasitario = timezone.now()
        patente.save()
        log_modificar(request.user.id, patente, 'Entrega de Antiparasitario')
        return HttpResponse("El retiro de antiparasitario se registro correctamente")


@login_required(login_url='login')
def alta_patente(request):
    if request.method == 'POST':
        form = PatenteForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        if form.is_valid() & mascota_form.is_valid() & detalle_mov_form.is_valid():
            patente = form.save(commit=False)
            patente.mascota = mascota_form.save()
            patente.fecha_vencimiento = timezone.now().date() + relativedelta(years=1)
            patente.save()
            detalle_mov = detalle_mov_form.save(commit=False)
            detalle_mov.completar(pd_m.Servicio.objects.get(nombre="Registro/patente anual"), patente)
            log_crear(request.user.id, patente, 'Patente')
            return redirect('patentes:lista_patentes')
    else:
        form = PatenteForm
        mascota_form = MascotaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
    return render(request, "patente/patente_form.html", {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                         'mascota_form': mascota_form})


class PdfCarnet(LoginRequiredMixin, PDFTemplateView):
    template_name = 'patente/carnet_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        patente = Patente.objects.get(pk=pk)
        return super(PdfCarnet, self).get_context_data(
            pagesize="A4",
            patente=patente
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
            log_crear(request.user.id, form.save(), 'Patente')
            return redirect('patentes:lista_patentes')
    else:
        form = ModificacionPatenteForm(instance=patente)
    return render(request, 'patente/patente_form.html', {'form': form, 'modificacion': True})


@login_required(login_url='login')
def reno_dup_patente(request, pk):
    patente = Patente.objects.get(pk=pk)
    if request.method == 'POST':
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        if detalle_mov_form.is_valid():
            detalle_mov = detalle_mov_form.save(commit=False)
            if request.POST['radio'] == 'renovacion':
                patente.fecha_vencimiento = timezone.now().date() + relativedelta(years=1)
                patente.save()
                servicio = pd_m.Servicio.objects.get(nombre="Renovacion de patente")
            else:
                servicio = pd_m.Servicio.objects.get(nombre="Duplicado de patente")
            detalle_mov.completar(servicio, patente)
            log_crear(request.user.id, patente, servicio.nombre)
            return redirect('patentes:lista_patentes')
    else:
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
    return render(request, 'patente/patente_reno_dup.html', {'detalle_mov_form': detalle_mov_form, 'patente': patente,
                                                             'fecha_hoy': timezone.now().date()})


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
        servicio_form = pd_f.ListaServicios(request.POST, tipo='Control Antirrabico')
        if form.is_valid() & detalle_mov_form.is_valid() & servicio_form.is_valid():
            control = form.save()
            detalle_mov = detalle_mov_form.save(commit=False)
            detalle_mov.completar(servicio_form.cleaned_data['servicio'], control)
            log_crear(request.user.id, control, 'Control Antirrabico')
            return redirect('controles:lista_controles')
    else:
        form = ControlAntirrabicoForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        servicio_form = pd_f.ListaServicios(tipo='Control Antirrabico')
    return render(request, 'control/control_form.html', {"form": form, 'detalle_mov_form': detalle_mov_form,
                                                         'servicio_form': servicio_form})


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
            control=control
        )


@login_required(login_url='login')
def lista_visitas_control(request, pk_control):
    lista_visitas = Visita.objects.filter(control__pk=pk_control)
    control = ControlAntirrabico.objects.get(pk=pk_control)
    dias_suceso = (timezone.now().date() - control.fecha_suceso).days
    ultima_visita = lista_visitas.last()
    apto_visita = True
    if dias_suceso > 10 or (ultima_visita and ultima_visita.fecha_visita == timezone.now().date()):
        apto_visita = False
    return render(request, 'control/visita_list.html', {'pk_control': pk_control, 'listado': lista_visitas,
                                                        'apto_visita': apto_visita})


@login_required(login_url='login')
def alta_visita(request, pk_control):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
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
    return render(request, 'retiroEntrega/retiroEntrega_list.html', {'listado': RetiroEntregaAnimal.objects.all()})


@login_required(login_url='login')
def alta_tramite(request):
    if 'tramite' in request.session:
        del request.session['tramite']
    if request.method == 'POST':
        form = RetiroEntregaForm(request.POST)
        if form.is_valid():
            retiro_entrega = form.save(commit=False)
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
        form = ListaPatentesForm(request.POST)
        if form.is_valid():
            patente = form.cleaned_data['patente']
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
        form = f.ListaPersonasGenericasForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        if form.is_valid() and mascota_form.is_valid():
            mascota = mascota_form.save()
            tramite = request.session['tramite']
            retiro_entrega = RetiroEntregaAnimal(tramite=tramite['tramite'], observaciones=tramite['observaciones'],
                                                 patentado=tramite['patentado'], mascota=mascota,
                                                 interesado=form.cleaned_data['persona'])
            if retiro_entrega.tramite == 'RETIRO':
                mascota.baja = True
                mascota.save()
            retiro_entrega.save()
            log_crear(request.user.id, retiro_entrega, 'Nuevo Retiro/Entrega de Animal no Patentado')
            return redirect('retiros_entregas:lista_retiro_entrega')
    else:
        form = f.ListaPersonasGenericasForm
        mascota_form = MascotaForm
    return render(request, 'retiroEntrega/retiroEntrega_noPatentado.html', {'form': form,
                                                                            'mascota_form': mascota_form})


@login_required(login_url='login')
def estadisticas_animales(request):
    rango_form = dp_f.RangoFechaForm
    years = [2018]
    if request.method == 'POST':
        rango_form = dp_f.RangoFechaForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']
            anio_desde = fecha_desde.year
            anio_hasta = fecha_hasta.year
            years = range(anio_hasta, anio_desde - 1, -1)

    todos_analisis = {}
    porker_analisis = {}
    lechon_analisis = {}
    adulto_analisis = {}

    for year in years:
        todos_analisis[str(year)] = Analisis.objects.filter(fecha__year=year).count()

        # acumuladores
        porker = 0
        lechon = 0
        adulto = 0

        categorias_analisis = Analisis.objects.filter(fecha__year=year).values_list("categoria")

        for categoria in categorias_analisis:
            if categoria[0] == "Porker":
                porker += 1
            elif categoria[0] == "Lechon":
                lechon += 1
            else:
                adulto += 1

        porker_analisis[str(year)] = porker
        lechon_analisis[str(year)] = lechon
        adulto_analisis[str(year)] = adulto

    ord_analisis = collections.OrderedDict(sorted(todos_analisis.items()))

    label_analisis = ord_analisis.keys()
    datos_analisis = ord_analisis.values()

    # Categorías análisis

    ord_porker_analisis = collections.OrderedDict(sorted(porker_analisis.items()))
    ord_lechon_analisis = collections.OrderedDict(sorted(lechon_analisis.items()))
    ord_adulto_analisis = collections.OrderedDict(sorted(adulto_analisis.items()))

    label_categoria_analisis = ord_adulto_analisis.keys()  # indistinto para los datos (tienen la misma clave)
    datos_porker = ord_porker_analisis.values()
    datos_lechon = ord_lechon_analisis.values()
    datos_adulto = ord_adulto_analisis.values()

    context = {
        'rango_form': rango_form,
        'promedio_analisis': int(np.average(datos_analisis)),
        'promedio_porkers': int(np.average(datos_porker)),
        'promedio_lechones': int(np.average(datos_lechon)),
        'promedio_adultos': int(np.average(datos_adulto)),
        # datos y etiquetas
        'lista_labels': json.dumps([label_analisis, label_categoria_analisis]),
        'lista_datos': json.dumps([{'Analisis': datos_analisis}, {'Porker': datos_porker, 'Lechon': datos_lechon,
                                                                  'Adulto': datos_adulto}])
    }

    return render(request, "estadistica/estadisticas_analisis.html", context)


@login_required(login_url='login')
def estadisticas_mascotas(request):
    rango_form = dp_f.RangoFechaForm
    years = [2018]
    if request.method == 'POST':
        rango_form = dp_f.RangoFechaForm(request.POST)
        if rango_form.is_valid():
            fecha_desde = rango_form.cleaned_data['fecha_desde']
            fecha_hasta = rango_form.cleaned_data['fecha_hasta']
            anio_desde = fecha_desde.year
            anio_hasta = fecha_hasta.year
            years = range(anio_hasta, anio_desde - 1, -1)

    patente_can_macho = {}
    patente_can_hembra = {}
    patente_fel_macho = {}
    patente_fel_hembra = {}
    esterilizacion_can_macho = {}
    esterilizacion_can_hembra = {}
    esterilizacion_fel_macho = {}
    esterilizacion_fel_hembra = {}
    entrega_animales = {}
    retiro_animales = {}

    for year in years:

        # acumuladores
        can_macho = 0
        can_hembra = 0
        fel_macho = 0
        fel_hembra = 0

        patentes_caninos = Patente.objects.filter(fecha__year=year).values_list(
            "mascota__categoria_mascota", "mascota__sexo")

        for patente in patentes_caninos:
            if (patente[0] == 'CANINA') and (patente[1] == 'Macho'):
                can_macho += 1
            elif (patente[0] == 'CANINA') and (patente[1] == 'Hembra'):
                can_hembra += 1
            elif (patente[0] == 'FELINA') and (patente[1] == 'Macho'):
                fel_macho += 1
            else:
                fel_hembra += 1

        patente_can_macho[str(year)] = can_macho
        patente_can_hembra[str(year)] = can_hembra
        patente_fel_macho[str(year)] = fel_macho
        patente_fel_hembra[str(year)] = fel_hembra

        # acumuladores
        can_macho = 0
        can_hembra = 0
        fel_macho = 0
        fel_hembra = 0

        esterilizaciones = Esterilizacion.objects.filter(turno__year=year).values_list(
            "mascota__categoria_mascota", "mascota__sexo")

        for esterilizacion in esterilizaciones:
            if (esterilizacion[0] == 'CANINA') and (esterilizacion[1] == 'Macho'):
                can_macho += 1
            elif (esterilizacion[0] == 'CANINA') and (esterilizacion[1] == 'Hembra'):
                can_hembra += 1
            elif (esterilizacion[0] == 'FELINA') and (esterilizacion[1] == 'Macho'):
                fel_macho += 1
            else:
                fel_hembra += 1

        esterilizacion_can_macho[str(year)] = can_macho
        esterilizacion_can_hembra[str(year)] = can_hembra
        esterilizacion_fel_macho[str(year)] = fel_macho
        esterilizacion_fel_hembra[str(year)] = fel_hembra

        # acumuladores
        entregas = 0
        retiros = 0

        animales_anio = RetiroEntregaAnimal.objects.filter(fecha__year=year).values_list("tramite")

        for animal in animales_anio:
            if animal[0] == "ENTREGA":
                entregas += 1
            elif animal[0] == "RETIRO":
                retiros += 1

        entrega_animales[str(year)] = entregas
        retiro_animales[str(year)] = retiros

    # patentamiento

    ord_patente_can_macho = collections.OrderedDict(sorted(patente_can_macho.items()))
    ord_patente_can_hembra = collections.OrderedDict(sorted(patente_can_hembra.items()))
    ord_patente_fel_macho = collections.OrderedDict(sorted(patente_fel_macho.items()))
    ord_patente_fel_hembra = collections.OrderedDict(sorted(patente_fel_hembra.items()))

    label_categoria_patente = ord_patente_can_macho.keys()  # indistinto para los datos (tienen la misma clave)
    datos_can_macho = ord_patente_can_macho.values()
    datos_can_hembra = ord_patente_can_hembra.values()
    datos_fel_macho = ord_patente_fel_macho.values()
    datos_fel_hembra = ord_patente_fel_hembra.values()

    # esterilizacion

    ord_esterilizacion_can_macho = collections.OrderedDict(sorted(esterilizacion_can_macho.items()))
    ord_esterilizacion_can_hembra = collections.OrderedDict(sorted(esterilizacion_can_hembra.items()))
    ord_esterilizacion_fel_macho = collections.OrderedDict(sorted(esterilizacion_fel_macho.items()))
    ord_esterilizacion_fel_hembra = collections.OrderedDict(sorted(esterilizacion_fel_hembra.items()))

    label_categoria_esterilizacion = ord_esterilizacion_can_macho.keys()  # indistinto para los datos (tienen la misma clave)
    datos_esterilizacion_can_macho = ord_esterilizacion_can_macho.values()
    datos_esterilizacion_can_hembra = ord_esterilizacion_can_hembra.values()
    datos_esterilizacion_fel_macho = ord_esterilizacion_fel_macho.values()
    datos_esterilizacion_fel_hembra = ord_esterilizacion_fel_hembra.values()

    # RETIRO Y ENTREGA DE ANIMALES

    ord_entrega_animales = collections.OrderedDict(sorted(entrega_animales.items()))
    ord_retiro_animales = collections.OrderedDict(sorted(retiro_animales.items()))

    label_animales_anios = ord_entrega_animales.keys()  # indistinto para los datos (tienen la misma clave)
    datos_entrega = ord_entrega_animales.values()
    datos_retiro = ord_retiro_animales.values()

    context = {
        'rango_form': rango_form,
        # mascotas
        'promedio_can_macho': int(np.average(datos_can_macho)),
        'promedio_can_hembra': int(np.average(datos_can_hembra)),
        'promedio_fel_macho': int(np.average(datos_fel_macho)),
        'promedio_fel_hembra': int(np.average(datos_fel_hembra)),
        # esterilizacion
        'promedio_esterilizacion_can_macho': int(np.average(datos_esterilizacion_can_macho)),
        'promedio_esterlizacion_can_hembra': int(np.average(datos_esterilizacion_can_hembra)),
        'promedio_esterlizacion_fel_macho': int(np.average(datos_esterilizacion_fel_macho)),
        'promedio_esterlizacion_fel_hembra': int(np.average(datos_esterilizacion_fel_hembra)),
        # retiros y entrega
        'promedio_entrega': int(np.average(datos_entrega)),
        'promedio_retiro': int(np.average(datos_retiro)),
        # datos y etiquetas
        'lista_labels': json.dumps([label_categoria_patente, label_categoria_esterilizacion, label_animales_anios]),
        'lista_datos': json.dumps([{'Can. Machos': datos_can_macho, 'Can. Hembras': datos_can_hembra,
                                    'Fel. Machos': datos_fel_macho, 'Fel. Hembras': datos_fel_hembra},
                                   {'Can. Machos': datos_esterilizacion_can_macho,
                                    'Can. Hembras': datos_esterilizacion_can_hembra,
                                    'Fel. Machos': datos_esterilizacion_fel_macho,
                                    'Fel. Hembras': datos_esterilizacion_fel_hembra},
                                   {'Entregados': datos_entrega, 'Retirados': datos_retiro}])
    }

    return render(request, "estadistica/estadisticas_mascotas.html", context)
