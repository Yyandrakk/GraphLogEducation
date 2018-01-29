from django.shortcuts import render
from django.urls import reverse_lazy

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
    models = models.CursoMoodle

    def get_queryset(self):
        return self.models.objects.filter(profesor_id=self.request.user.id)


class addCursoView(LoginRequiredMixin, generic.CreateView):
    template_name = "cursos/addCursos.html"
    models = models.CursoMoodle
    success_url = reverse_lazy("cursos:todos")
    context_object_name = "curso_add"