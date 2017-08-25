# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from .models import *
from .forms import *
from .filters import *
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)

@login_required(login_url='login')
def lista_abastecedor(request):
    lista_abastecedores = Abastecedor.objects.all()
    filtro_abastecedores = AbastecedorListFilter(request.GET, queryset=lista_abastecedores)
    return render(request, 'abastecedor/abastecedor_list.html', {'filter': filtro_abastecedores})


class AltaAbastecedor(LoginRequiredMixin, CreateView):
    model = Abastecedor
    template_name = 'abastecedor/abastecedor_form.html'
    success_url = reverse_lazy('abastecedores:lista_abastecedores')
    form_class = AbastecedorForm
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
