# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
import datetime
from .forms import *
from .filters import *
from .models import *
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
