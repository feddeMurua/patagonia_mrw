# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from .filters import *
from libreta_curso import models as m
from desarrollo_patagonia.utils import *
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url='login')
def lista_personas_fisicas(request):
    lista_personas = PersonaFisica.objects.all()
    filtro_personas = PersonaListFilter(request.GET, queryset=lista_personas)
    return render(request, 'persona/persona_fisica_list.html', {'filter': filtro_personas})


@login_required(login_url='login')
def alta_persona_fisica(request):
    if request.method == 'POST':
        form = AltaPersonaFisicaForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_crear(request.user.id, persona, 'Persona Física')
            return redirect('personas:lista_personas_fisicas')
    else:
        form = AltaPersonaFisicaForm
        domicilio_form = DomicilioForm
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_personas_fisicas'})


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
        domicilio_form = DomicilioForm(instance=persona.domicilio)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_modificar(request.user.id, persona, 'Persona Física')
            return redirect('personas:lista_personas_fisicas')
    else:
        form = ModificacionPersonaFisicaForm(instance=persona)
        domicilio_form = DomicilioForm(instance=persona.domicilio)
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_personas_fisicas'})


@login_required(login_url='login')
def detalle_persona_fisica(request, id_persona):
    persona = PersonaFisica.objects.get(id=id_persona)
    lista_cursos_inscripciones = m.Inscripcion.objects.filter(persona__id=id_persona)
    return render(request, "persona/persona_fisica_detail.html", {'persona': persona,
                                                                  'inscripciones': lista_cursos_inscripciones})


@login_required(login_url='login')
def lista_personas_juridicas(request):
    lista_personas = PersonaJuridica.objects.all()
    filtro_personas = PersonaJuridicaListFilter(request.GET, queryset=lista_personas)
    return render(request, 'persona/persona_juridica_list.html', {'filter': filtro_personas})


@login_required(login_url='login')
def alta_persona_juridica(request):
    if request.method == 'POST':
        form = AltaPersonaJuridicaForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_crear(request.user.id, persona, 'Persona Jurídica')
            return redirect('personas:lista_personas_juridicas')
    else:
        form = AltaPersonaJuridicaForm
        domicilio_form = DomicilioForm
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_personas_juridicas'})


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
        domicilio_form = DomicilioForm(instance=persona.domicilio)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_modificar(request.user.id, persona, 'Persona Jurídica')
            return redirect('personas:lista_personas_juridicas')
    else:
        form = ModificacionPersonaJuridicaForm(instance=persona)
        domicilio_form = DomicilioForm(instance=persona.domicilio)
    return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form,
                                                         'url_return': 'personas:lista_personas_juridicas'})


@login_required(login_url='login')
def lista_personal_propio(request):
    lista_personas = PersonalPropio.objects.all()
    filtro_personas = PersonalPropioListFilter(request.GET, queryset=lista_personas)
    return render(request, 'persona/personal_propio_list.html', {'filter': filtro_personas})


@login_required(login_url='login')
def alta_personal_propio(request):
    if request.method == 'POST':
        form = AltaPersonalPropioForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
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
        domicilio_form = DomicilioForm(instance=persona.domicilio)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_modificar(request.user.id, persona, 'Personal Propio')
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
