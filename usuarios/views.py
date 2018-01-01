# Create your views here.

from django.shortcuts import render

from .forms import FormRegister, FormLogin


def form_login_view(request):

    form = FormLogin()

    return render(request, 'usuarios/login.html', context={form:form})

def form_register_view(request):

    form = FormRegister()

    if request.method == "POST":
        form = FormRegister(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return form_login_view()
        else:
            print('Error form invalid')


    return render(request,'usuarios/register.html',context={form:form})
