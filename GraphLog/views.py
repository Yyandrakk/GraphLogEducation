from django.shortcuts import render
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.views import generic

# Create your views here.

class indexView(LoginRequiredMixin,generic.TemplateView):
    template_name = "GraphLog/index.html"
