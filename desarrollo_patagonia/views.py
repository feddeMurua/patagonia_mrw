from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# def get_order(get):
#     if "o" in get:
#         return get["o"]


# @login_required(login_url='registration')
def inicio(request):
    return render(request, "base/inicio.html")
