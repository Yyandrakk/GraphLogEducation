# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import FormRegister


class SignUpView(CreateView):
    form_class = FormRegister
    success_url = reverse_lazy("user:login")
    template_name ="usuarios/register.html"
