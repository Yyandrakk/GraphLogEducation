# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import FormRegister, FormLogin


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(''))

def form_login_view(request):

    if request.method == 'POST':
       form = FormLogin(request.POST)
       if form.is_valid():
           username = form.username
           password = form.password
           usuario = authenticate(username=username,password=password)
           if usuario:
               if usuario.is_active:
                   login(request,usuario)
                   return HttpResponseRedirect(reverse('index'))
               else:
                   return HttpResponse("Cuenta no activada")
           else:
               return HttpResponse("Error en el login")
    else:
        form = FormLogin();

    return render(request, 'usuarios/login.html', context={"form":form})

def form_register_view(request):

    form = FormRegister()

    if request.method == "POST":
        form = FormRegister(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return form_login_view()
        else:
            print('Error form invalid')


    return render(request,'usuarios/register.html',context={"form":form})
