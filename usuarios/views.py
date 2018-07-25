from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from desarrollo_patagonia.utils import *
from .forms import *
from usuarios.models import CustomUser


class CustomPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('cambio_password_hecho')


@login_required(login_url='login')
def lista_usuarios(request):
    return render(request, 'usuarios/usuario_list.html', {'listado': User.objects.filter(is_superuser=False)})


@login_required(login_url='login')
def alta_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            log_crear(request.user.id, form.save(), 'Usuario')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm
    return render(request, 'usuarios/usuario_form.html', {'form': form})


@login_required(login_url='login')
def baja_usuario(request, pk):
    usuario = CustomUser.objects.get(pk=pk)
    log_eliminar(request.user.id, usuario, 'Usuario')
    usuario.delete()
    return HttpResponse()


@login_required(login_url='login')
def modificar_usuario(request, pk):
    usuario = CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            log_modificar(request.user.id, form.save(), 'Usuario')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form})
