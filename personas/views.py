# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from desarrollo_patagonia.utils import *
from libreta_curso import models as lc_m
from animales import models as a_m
from django.views.generic import DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_addanother.views import CreatePopupMixin


@login_required(login_url='login')
def lista_contribuyentes(request):
    return render(request, 'persona/contribuyente_list.html', {'listado': PersonaGenerica.objects.all()})


@login_required(login_url='login')
def alta_p_fisica(request):
    if request.method == 'POST':
        form = AltaPersonaFisicaForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_crear(request.user.id, persona, 'Persona Física')
            return redirect('personas:lista_contribuyentes')
    else:
        form = AltaPersonaFisicaForm
        domicilio_form = DomicilioForm
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_contribuyentes'})


@login_required(login_url='login')
def baja_persona_fisica(request, pk):
    persona = PersonaFisica.objects.get(pk=pk)
    log_eliminar(request.user.id, persona, 'Persona Física')
    persona.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_persona_fisica(request, pk):
    persona = PersonaFisica.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionPersonaFisicaForm(request.POST, instance=persona)
        domicilio_form = DomicilioForm(request.POST, instance=persona.domicilio)
        if form.is_valid() & domicilio_form.is_valid():
            domicilio_form.save()
            log_modificar(request.user.id, form.save(), 'Persona Física')
            return redirect('personas:lista_contribuyentes')
    else:
        form = ModificacionPersonaFisicaForm(instance=persona)
        domicilio_form = DomicilioForm(instance=persona.domicilio)
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_contribuyentes'})


@login_required(login_url='login')
def detalle_persona_fisica(request, pk):
    persona = PersonaFisica.objects.get(pk=pk)
    libreta = lc_m.LibretaSanitaria.objects.filter(persona=persona).last()
    inscripcion = None
    if libreta:
        inscripcion = lc_m.Inscripcion.objects.filter(curso=libreta.curso).last()
    patentes = a_m.Patente.objects.filter(persona=persona)
    return render(request, "persona/persona_fisica_detail.html", {"persona": persona, "libreta": libreta,
                                                                  "inscripcion": inscripcion, "patentes": patentes})


@login_required(login_url='login')
def alta_p_juridica(request):
    if request.method == 'POST':
        form = AltaPersonaJuridicaForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_crear(request.user.id, persona, 'Persona Jurídica')
            return redirect('personas:lista_contribuyentes')
    else:
        form = AltaPersonaJuridicaForm
        domicilio_form = DomicilioForm
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_contribuyentes'})


class DetallePersonaJuridica(LoginRequiredMixin, DetailView):
    model = PersonaJuridica
    template_name = "persona/persona_juridica_detail.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


@login_required(login_url='login')
def baja_persona_juridica(request, pk):
    persona = PersonaJuridica.objects.get(pk=pk)
    log_eliminar(request.user.id, persona, 'Persona Jurídica')
    persona.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_persona_juridica(request, pk):
    persona = PersonaJuridica.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionPersonaJuridicaForm(request.POST, instance=persona)
        domicilio_form = DomicilioForm(request.POST, instance=persona.domicilio)
        if form.is_valid() & domicilio_form.is_valid():
            domicilio_form.save()
            log_modificar(request.user.id, form.save(), 'Persona Jurídica')
            return redirect('personas:lista_contribuyentes')
    else:
        form = ModificacionPersonaJuridicaForm(instance=persona)
        domicilio_form = DomicilioForm(instance=persona.domicilio)
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_contribuyentes'})


@login_required(login_url='login')
def lista_personal_propio(request):
    return render(request, 'persona/personal_propio_list.html', {'listado': PersonalPropio.objects.all()})


@login_required(login_url='login')
def alta_p_propio(request):
    if request.method == 'POST':
        form = AltaPersonalPropioForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            form.save_m2m()
            log_crear(request.user.id, persona, 'Personal Propio')
            return redirect('personas:lista_personal_propio')
    else:
        form = AltaPersonalPropioForm
        domicilio_form = DomicilioForm
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_personal_propio'})


@login_required(login_url='login')
def baja_personal_propio(request, pk):
    persona = PersonalPropio.objects.get(pk=pk)
    log_eliminar(request.user.id, persona, 'Personal Propio')
    persona.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_personal_propio(request, pk):
    persona = PersonalPropio.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionPersonalPropioForm(request.POST, instance=persona)
        domicilio_form = DomicilioForm(request.POST, instance=persona.domicilio)
        if form.is_valid() & domicilio_form.is_valid():
            domicilio_form.save()
            log_modificar(request.user.id, form.save(), 'Personal Propio')
            return redirect('personas:lista_personal_propio')
    else:
        form = ModificacionPersonalPropioForm(instance=persona)
        domicilio_form = DomicilioForm(instance=persona.domicilio)
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_personal_propio'})


class DetallePersonalPropio(LoginRequiredMixin, DetailView):
    model = PersonalPropio
    template_name = "persona/personal_propio_detail.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaLocalidad(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = Localidad
    form_class = LocalidadForm
    template_name = "domicilio/localidad_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaProvincia(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = Provincia
    fields = '__all__'
    template_name = "domicilio/provincia_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class AltaNacionalidad(LoginRequiredMixin, CreatePopupMixin, CreateView):
    model = Nacionalidad
    fields = '__all__'
    template_name = "domicilio/nacionalidad_form.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
