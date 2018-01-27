from django.shortcuts import render
from . import models
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.views import generic
# Create your views here.

class indexCursoView(LoginRequiredMixin,generic.ListView):
    template_name = "cursos/listCursos.html"
    context_object_name = 'curso_list'
    models = models.CursoMoodle.objects

    def get_queryset(self):
        queryset = super(indexCursoView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset