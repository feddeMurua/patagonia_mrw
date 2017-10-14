# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from .filters import *
from libreta_curso import models as m
from desarrollo_patagonia.utils import *


@login_required(login_url='login')
def lista_persona(request):
    lista_personas = PersonaFisica.objects.all()
    filtro_personas = PersonaListFilter(request.GET, queryset=lista_personas)
    return render(request, 'persona/persona_list.html', {'filter': filtro_personas})


@login_required(login_url='login')
def lista_detalles_persona(request, id_persona):
    persona = PersonaFisica.objects.get(id=id_persona)
    lista_cursos_inscripciones = m.Inscripcion.objects.filter(persona__id=id_persona)
    return render(request, "persona/persona_detail.html", {'persona': persona,
                                                           'inscripciones': lista_cursos_inscripciones})


@login_required(login_url='login')
def alta_persona(request):
    if request.method == 'POST':
        form = AltaPersonaFisicaForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if form.is_valid() & domicilio_form.is_valid():
            persona = form.save(commit=False)
            persona.domicilio = domicilio_form.save()
            persona.save()
            log_crear(request.user.id, persona, 'Persona Física')
            return redirect('personas:lista_personas')
        else: # no se verifica que alguno (o los dos) de los dos form sea valido
            return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form})
    else:
        form = AltaPersonaFisicaForm
        domicilio_form = DomicilioForm
        return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form})


@login_required(login_url='login')
def baja_persona(request, pk):
    persona = PersonaFisica.objects.get(pk=pk)
    log_eliminar(request.user.id, persona, 'Persona Física')
    persona.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificacion_persona(request, pk):
    persona = PersonaFisica.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionPersonaFisicaForm(request.POST, instance=persona)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Persona Física')
            return redirect('personas:lista_personas')
    else:
        form = ModificacionPersonaFisicaForm(instance=persona)
        domicilio_form = DomicilioForm(instance=persona.domicilio)
        return render(request, "persona/persona_form.html", {'form': form, 'domicilio_form': domicilio_form})
