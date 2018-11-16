# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from easy_pdf.views import PDFTemplateView
from .forms import *
from .models import *
from desarrollo_patagonia.utils import *
from parte_diario_caja import forms as pd_f
from parte_diario_caja import views as pd_v
from desarrollo_patagonia import forms as dp_f
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from dateutil.relativedelta import *
from django.utils import timezone
import json
import collections
from parte_diario_caja.models import DetalleMovimiento
from base64 import b64decode
from django.core.files.base import ContentFile


'''
CURSOS
'''


@login_required(login_url='login')
def lista_curso(request):
    return render(request, 'curso/curso_list.html', {'fecha_hoy': timezone.now().date(), 'listado': Curso.objects.all()})


@login_required(login_url='login')
def alta_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, usuario=request.user)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Curso de Manipulacion de Alimentos')
            return redirect('cursos:lista_cursos')
    else:
        form = CursoForm
    return render(request, 'curso/curso_form.html', {'form': form})


@staff_member_required
@login_required(login_url='login')
def baja_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    log_eliminar(request.user.id, curso, 'Curso de Manipulacion de Alimentos')
    curso.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionCursoForm(request.POST, instance=curso, usuario=request.user)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Curso de Manipulacion de Alimentos')
            return redirect('cursos:lista_cursos')
    else:
        form = ModificacionCursoForm(instance=curso)
    return render(request, 'curso/curso_form.html', {'form': form, 'modificacion': True})


@login_required(login_url='login')
def cierre_de_curso(request, id_curso):
    if request.method == 'POST':
        curso = Curso.objects.get(pk=id_curso)
        curso.finalizado = True
        curso.save()
        log_modificar(request.user.id, curso, 'Cierre de Curso')
        return redirect('cursos:lista_cursos')
    else:
        lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
        apto_cierre = True
        for inscripcion in lista_inscripciones:
            if not inscripcion.modificado:
                apto_cierre = False
                break
        return render(request, "curso/curso_cierre.html", {'id_curso': id_curso, 'listado': lista_inscripciones,
                                                           'apto_cierre': apto_cierre})


class PdfAsistencia(LoginRequiredMixin, PDFTemplateView):
    template_name = 'curso/planilla_asistencia_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        curso = Curso.objects.get(pk=pk)
        return super(PdfAsistencia, self).get_context_data(
            curso=curso,
            inscripciones=Inscripcion.objects.filter(curso=curso),
            title='Planilla de asistencia a curso N°'
        )


class PdfAprobados(LoginRequiredMixin, PDFTemplateView):
    template_name = 'curso/aprobados_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        curso = Curso.objects.get(pk=pk)
        return super(PdfAprobados, self).get_context_data(
            curso=curso,
            inscripciones=Inscripcion.objects.filter(curso=curso, calificacion="Aprobado"),
            title='Planilla de aprobados de curso N°'
        )


'''
INSCRIPCIONES
'''


@login_required(login_url='login')
def lista_inscripciones_curso(request, id_curso):
    lista_inscripciones = Inscripcion.objects.filter(curso__pk=id_curso)
    curso = Curso.objects.get(pk=id_curso)
    inscriptos = len(lista_inscripciones)
    return render(request, "curso/curso_inscripciones.html", {'fecha_hoy': timezone.now().date(), 'curso': curso,
                                                              'inscriptos': inscriptos, 'listado': lista_inscripciones})


@login_required(login_url='login')
def alta_inscripcion(request, id_curso):
    if request.method == 'POST':
        form = InscripcionForm(request.POST, id_curso=id_curso)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.curso = Curso.objects.get(pk=id_curso)
            inscripcion.save()
            log_crear(request.user.id, inscripcion, 'Inscripcion a Curso')
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', kwargs={'id_curso': id_curso}))
    else:
        form = InscripcionForm
    url_return = 'cursos:inscripciones_curso'
    return render(request, "inscripcion/inscripcion_form.html", {'id_curso': id_curso, 'url_return': url_return,
                                                                 'form': form})


@login_required(login_url='login')
def baja_inscripcion(request, pk):
    inscripcion = Inscripcion.objects.get(pk=pk)
    log_eliminar(request.user.id, inscripcion, 'Inscripcion a Curso')
    inscripcion.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_inscripcion(request, pk, id_curso):
    inscripcion = Inscripcion.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionInscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Inscripcion a Curso')
            return HttpResponseRedirect(reverse('cursos:inscripciones_curso', kwargs={'id_curso': id_curso}))
    else:
        form = ModificacionInscripcionForm(instance=inscripcion)
    return render(request, 'inscripcion/inscripcion_form.html', {'form': form, 'id_curso': id_curso,
                                                                 'url_return': 'cursos:inscripciones_curso',
                                                                 'modificacion': True})


@login_required(login_url='login')
def cierre_inscripcion(request, pk, id_curso):
    inscripcion = Inscripcion.objects.get(pk=pk)
    if request.method == 'POST':
        form = CierreInscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            cierre = form.save(commit=False)
            cierre.modificado = True
            cierre.save()
            log_modificar(request.user.id, cierre, 'Calificacion de Inscripcion en Curso')
            return HttpResponseRedirect(reverse('cursos:cierre_curso', kwargs={'id_curso': id_curso}))
    else:
        form = CierreInscripcionForm(instance=inscripcion)
    return render(request, 'inscripcion/inscripcion_form.html', {'form': form, 'id_curso': id_curso,
                                                                 'url_return': 'cursos:cierre_curso',
                                                                 'modificacion': True})


class PdfInscripcion(LoginRequiredMixin, PDFTemplateView):
    template_name = 'inscripcion/inscripcion_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        inscripcion = Inscripcion.objects.get(pk=pk)
        return super(PdfInscripcion, self).get_context_data(
            inscripcion=inscripcion,
            title='Comprobante de inscripcion a curso N° ' + str(inscripcion.curso.pk)
        )


'''
LIBRETRAS SANITARIAS
'''


def get_cursos(pk_persona):
    inscripciones = Inscripcion.objects.filter(persona__pk=pk_persona)
    cursos = []
    for inscripcion in inscripciones:
        if inscripcion.calificacion == 'Aprobado':
            cursos.append(inscripcion.curso)
    return cursos


@login_required(login_url='login')
def lista_libreta(request):
    return render(request, 'libreta/libreta_list.html', {'listado': LibretaSanitaria.objects.all(),
                                                         'fecha_hoy': timezone.now()})


def img_to_base64(data,usr):
    formato, imgstr = data.split(';base64,')
    ext = formato.split('/')[-1]
    return ContentFile(b64decode(imgstr), name=usr + '.' + ext)  # You can save this as file instance.


@login_required(login_url='login')
def alta_libreta(request):
    mensaje = ''
    if request.method == 'POST':
        form = LibretaForm(request.POST, request.FILES)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if form.is_valid():
            libreta = form.save(commit=False)
            cursos = get_cursos(libreta.persona.pk)
            if not cursos and libreta.tipo_libreta == "Blanca":
                mensaje = 'No es posible expedir una libreta BLANCA sin un curso previo'
            else:
                if libreta.tipo_libreta != 'Celeste':
                    libreta.fecha_vencimiento = libreta.fecha_examen_clinico + relativedelta(years=1)
                else:
                    libreta.fecha_vencimiento = libreta.fecha_examen_clinico + relativedelta(
                        months=int(request.POST['meses']))
                if cursos:
                    libreta.curso = cursos[-1]
                '''
                if request.POST['foto'] and request.POST['foto'] != "borrar":
                    libreta.foto = img_to_base64(request.POST['foto'], libreta.persona.dni)
                '''
                if request.POST['optradio'] == 'previa':
                    if detalle_mov_form.is_valid():
                        libreta.save()
                        pd_v.movimiento_previo(request, detalle_mov_form, "Alta de libreta sanitaria", libreta,
                                               'Libreta Sanitaria')
                        return redirect('libretas:lista_libretas')
                else:
                    if mov_form.is_valid():
                        libreta.save()
                        pd_v.nuevo_movimiento(request, mov_form, "Alta de libreta sanitaria", libreta, 'Libreta Sanitaria')
                        return redirect('libretas:lista_libretas')
    else:
        form = LibretaForm
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'libreta/libreta_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                         'mov_form': mov_form, 'mensaje': mensaje})


class DetalleLibreta(LoginRequiredMixin, DetailView):
    model = LibretaSanitaria
    template_name = 'libreta/libreta_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@staff_member_required
@login_required(login_url='login')
def baja_libreta(request, pk):
    libreta = LibretaSanitaria.objects.get(pk=pk)
    log_eliminar(request.user.id, libreta, 'Libreta Sanitaria')
    libreta.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_libreta(request, pk):
    libreta = LibretaSanitaria.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionLibretaForm(request.POST, instance=libreta)
        if form.is_valid():
            libreta = form.save(commit=False)
            '''
            if request.POST['foto'] == 'borrar':
                libreta.foto = None
            elif request.POST['foto'] == 'borrar':
                libreta.foto = img_to_base64(request.POST['foto'], libreta.persona.dni)
            '''
            libreta.save()
            log_modificar(request.user.id, libreta, 'Libreta Sanitaria')
            return redirect('libretas:lista_libretas')
    else:
        form = ModificacionLibretaForm(instance=libreta)
    return render(request, 'libreta/libreta_form.html', {'form': form, 'libreta': libreta, 'modificacion': True})


@login_required(login_url='login')
def renovacion_libreta(request, pk):
    mensaje = ''
    libreta = LibretaSanitaria.objects.get(pk=pk)
    if request.method == 'POST':
        form = RenovacionLibretaForm(request.POST, instance=libreta)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm(request.POST)
        mov_form = pd_f.MovimientoDiarioForm(request.POST)
        if form.is_valid():
            libreta = form.save(commit=False)
            cursos = get_cursos(libreta.persona.pk)
            if libreta.tipo_libreta == 'Amarilla':
                mensaje = 'No es posible renovar libretas AMARILLAS'
            elif not cursos and libreta.tipo_libreta == "Celeste":
                mensaje = 'No es posible renovar una libreta CELESTE sin un curso previo'
            else:
                libreta.curso = cursos[-1]
                libreta.fecha_vencimiento = libreta.fecha_examen_clinico + relativedelta(years=1)
                libreta.tipo_libreta = 'Blanca'
                '''
                if request.POST['foto'] == 'borrar':
                    libreta.foto = None
                elif request.POST['foto'] == 'borrar':
                    libreta.foto = img_to_base64(request.POST['foto'], libreta.persona.dni)
                '''
                if request.POST['optradio'] == 'previa':
                    if detalle_mov_form.is_valid():
                        libreta.save()
                        pd_v.movimiento_previo(request, detalle_mov_form, "Renovacion de libreta sanitaria", libreta,
                                               'Renovacion de Libreta Sanitaria')
                        return redirect('libretas:lista_libretas')
                else:
                    if mov_form.is_valid():
                        libreta.save()
                        pd_v.nuevo_movimiento(request, mov_form, "Renovacion de libreta sanitaria", libreta,
                                              'Renovacion de Libreta Sanitaria')
                        return redirect('libretas:lista_libretas')
    else:
        form = RenovacionLibretaForm(instance=libreta)
        detalle_mov_form = pd_f.DetalleMovimientoDiarioForm
        mov_form = pd_f.MovimientoDiarioForm
    return render(request, 'libreta/libreta_form.html', {'form': form, 'detalle_mov_form': detalle_mov_form,
                                                         'mov_form': mov_form, 'libreta': libreta, 'mensaje': mensaje})


class PdfLibreta(LoginRequiredMixin, PDFTemplateView):
    template_name = 'libreta/libreta_pdf.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_context_data(self, pk):
        return super(PdfLibreta, self).get_context_data(
            libreta=LibretaSanitaria.objects.get(pk=pk),
            title='Libreta sanitaria N°'
        )


'''
ESTADÍSTICAS
'''


@login_required(login_url='login')
def estadisticas_lc(request):
    rango_form = dp_f.RangoAnioForm
    years = [timezone.now().year]
    if request.method == 'POST':
        rango_form = dp_f.RangoAnioForm(request.POST)
        if rango_form.is_valid():
            years = range(int(rango_form.cleaned_data['anio_hasta']),
                          int(rango_form.cleaned_data['anio_desde']) - 1, -1)

    # CURSOS POR AÑO
    cursos_anuales = {}
    for year in years:
        cursos_anuales[str(year)] = Curso.objects.filter(fecha__year=year).count()
    ord_cursos_anuales = collections.OrderedDict(sorted(cursos_anuales.items()))
    label_year = ord_cursos_anuales.keys()
    datos_cursos_anuales = ord_cursos_anuales.values()

    # INSCRIPCIONES A CURSO
    inscripciones = to_counter(Inscripcion, {'curso__fecha__year__lte': years[0], 'curso__fecha__year__gte': years[-1]},
                               ['curso__fecha'])

    # CALIFICACIONES POR CURSO
    calificaciones = to_counter(Inscripcion, {'curso__fecha__year__lte': years[0], 'curso__fecha__year__gte': years[-1],
                                              'curso__finalizado': True}, ['calificacion'])

    # LIBRETAS POR TIPO
    libretas_tipo = to_counter(LibretaSanitaria, {'fecha__year__lte': years[0], 'fecha__year__gte': years[-1]},
                               ['tipo_libreta'])

    # LIBRETAS POR SERVICIO
    libretas_servicio = to_counter(DetalleMovimiento, {'movimiento__fecha__year__lte': years[0],
                                                       'movimiento__fecha__year__gte': years[-1],
                                                       'servicio__in': ['Alta de libreta sanitaria',
                                                                        'Renovacion de libreta sanitaria']},
                                   ['servicio'])
    key_inscripciones = []
    for fecha in inscripciones:
        key_inscripciones.append(fecha[0].strftime('%d-%m-%Y'))
    context = {
        'rango_form': rango_form,
        # datos y etiquetas
        'lista_labels': json.dumps([key_inscripciones, label_year, calificaciones.keys(), libretas_tipo.keys(),
                                    libretas_servicio.keys()]),
        'lista_datos': json.dumps([{'Inscripciones': inscripciones.values()}, {'Cursos': datos_cursos_anuales},
                                   {'Calificaciones Curso': calificaciones.values()},
                                   {'Tipo Libretas': libretas_tipo.values()},
                                   {'Servicio Libretas': libretas_servicio.values()}])
    }
    return render(request, "estadistica/estadisticas_lc.html", context)
