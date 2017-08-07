# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from easy_pdf.views import PDFTemplateView
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
    print lista_analisis
    filtro_analisis = AnalisisListFilter(request.GET, queryset=lista_analisis)
    fecha_hoy = datetime.date.today()
    return render(request, 'analisis/analisis_list.html', {'fecha_hoy': fecha_hoy, 'filter': filtro_analisis})


class AltaAnalisis(LoginRequiredMixin, CreateView):
    model = Analisis
    template_name = 'analisis/analisis_form.html'
    success_url = reverse_lazy('analisis:lista_analisis')
    form_class = AnalisisForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BajaAnalisis(LoginRequiredMixin, DeleteView):
    model = Analisis
    template_name = 'analisis/analisis_confirm_delete.html'
    success_url = reverse_lazy('analisis:lista_analisis')
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class DetalleAnalisis(LoginRequiredMixin, DetailView):
    model = Analisis
    template_name = 'analisis/analisis_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
