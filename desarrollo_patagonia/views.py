from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def inicio(request):
    return render(request, "base/inicio.html")

