# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from .forms import *
from .filters import *
from libreta_curso import models as m
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)


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


def alta_persona(request):
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)
        if persona_form.is_valid() & domicilio_form.is_valid():
            persona = persona_form.save(commit=False)
            domicilio = domicilio_form.save(commit=False)
            domicilio.save()
            persona.domicilio = domicilio
            persona.save()
            return redirect('personas:lista_personas')
    else:
        persona_form = PersonaForm
        domicilio_form = DomicilioForm
        return render(request, "persona/persona_form.html", {'persona_form': persona_form,
                                                             'domicilio_form': domicilio_form})


class BajaPersona(LoginRequiredMixin, DeleteView):
    model = PersonaFisica
    template_name = 'persona/persona_confirm_delete.html'
    success_url = reverse_lazy('personas:lista_personas')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class ModificacionPersona(LoginRequiredMixin, UpdateView):
    model = PersonaFisica
    template_name = 'persona/persona_form.html'
    success_url = reverse_lazy('personas:lista_personas')
    fields = ['obra_social', 'domicilio', 'telefono', 'email', 'rubro', 'documentacion_retirada']
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

