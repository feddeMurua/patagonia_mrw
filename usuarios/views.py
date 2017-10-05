from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from .forms import *


class CustomPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('cambio_password_hecho')


@login_required(login_url='login')
def alta_usuario(request):
    if request.method == 'POST':
        form = AltaUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = AltaUsuarioForm
    return render(request, 'usuarios/usuario_form.html', {'form': form})