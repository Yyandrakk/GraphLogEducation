# Create your views here.
from django.views.generic import CreateView

from .forms import FormRegister


class SignUpView(CreateView):
    form_class = FormRegister
    success_url = "user:login"
    template_name ="usuarios/register.html"
