from random import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify

from cursos.models import CursoMoodle
from . import models
from .forms import FormCursoMoodle
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



def unique_slug_generator(slug):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """

    if CursoMoodle.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{rand}".format(
            slug=slug,
            rand=random.randint(0,1000)
        )
        return unique_slug_generator(slug=new_slug)
    return slug

class addCursoView(LoginRequiredMixin, generic.CreateView):
    template_name = "cursos/addCursos.html"
    form_class = FormCursoMoodle
    success_url = reverse_lazy("cursos:todos")

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.profesor = self.request.user
        self.object.slug = unique_slug_generator(slugify(self.object.nombre))
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(addCursoView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
