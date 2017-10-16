from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from desarrollo_patagonia.utils import *
from .forms import *


class CustomPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('cambio_password_hecho')


@login_required(login_url='login')
def lista_usuarios(request):
    listado_usuarios = User.objects.filter(is_superuser=False)
    return render(request, 'usuarios/usuario_list.html', {'usuarios': listado_usuarios})


@login_required(login_url='login')
def alta_usuario(request):
    if request.method == 'POST':
        form = AltaUsuarioForm(request.POST)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Usuario')
            return redirect('lista_usuarios')
    else:
        form = AltaUsuarioForm
    return render(request, 'usuarios/usuario_form.html', {'form': form})


@login_required(login_url='login')
def baja_usuario(request, pk):
    usuario = User.objects.get(pk=pk)
    log_eliminar(request.user.id, usuario, 'Usuario')
    usuario.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificar_usuario(request, pk):
    usuario = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModificacionUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Usuario')
            return redirect('lista_usuarios')
    else:
        form = ModificacionUsuarioForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form})