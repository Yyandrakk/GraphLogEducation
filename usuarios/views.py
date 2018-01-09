# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

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
               return HttpResponse("Error en el formulario")
       else:
           return HttpResponse("Error en el form")
    else:
        form = FormLogin();

    return render(request, 'usuarios/login.html', context={"form":form})

class RegisterView(TemplateView):
    template_name = 'usuarios/register.html'

    def get_context_data(self, **kwargs):
        




def form_register_view(request):



    if request.method == "POST":
        form = FormRegister(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse(''))
        else:
            print(form.errors)
            return HttpResponse("Error en el registro")
    else:
        form = FormRegister()

    return render(request,'usuarios/register.html',context={"form":form})
