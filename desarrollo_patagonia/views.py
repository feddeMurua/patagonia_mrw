from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView


@login_required(login_url='login')
def inicio(request):
    return render(request, "base/inicio.html")


class CustomPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('cambio_password_hecho')