from random import random

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify


from cursos.models import CursoMoodle, TiempoDedicadoCursoMoodle
from . import models
from .forms import FormCursoMoodle
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views import generic

class indexCursoView(LoginRequiredMixin,generic.ListView):
    template_name = "cursos/listCursos.html"
    context_object_name = 'curso_list'
    models = models.CursoMoodle

    def get_queryset(self):
        return self.models.objects.filter(profesor_id=self.request.user.id)

def unique_slug_generator(slug):

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


class detailCursoView(LoginRequiredMixin ,generic.DetailView):
    template_name = "cursos/detailCurso.html"
    model = models.CursoMoodle
    context_object_name = 'curso'

    def user_test(self,request,slug):
        return models.CursoMoodle.objects.filter(slug=slug,profesor_id=request.user.id).exists()


    def dispatch(self, request, *args, **kwargs):
        if not self.user_test(request,kwargs.get('slug','')):
            return redirect("cursos:todos")
        return super().dispatch(
            request, *args, **kwargs)


def createChart(type,labels,data,tittle,label):
    '''
    :param type: Tipo de grafico
    :param labels: Etiquetas del eje x
    :param data: Datos del eje y
    :param tittle: Titulo del grafico
    :param label: Leyenda
    :return:
    '''

def ajaxCharts(request):
    charts=[]
    id = request.GET.get('id', None)
    if id != None and CursoMoodle.objects.filter(pk=id).exists():
        dias = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id,tipo=TiempoDedicadoCursoMoodle.DIA)
        chart = {'type': 'line'}
        labels = []
        data = []
        for dia in dias:
            labels.append(format(dia.timestamp,"%d/%m/%Y"))
            data.append(dia.contador)
        chart['data'] = {'labels':labels,'datasets':[{'data':data, 'label':'Eventos'}]}
        charts.append(chart)

        chart = {'type': 'bar'}
        labels = []
        data = []
        horas = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id, tipo=TiempoDedicadoCursoMoodle.HORA)
        for hora in horas:
            labels.append(format(hora.timestamp,"%H"))
            data.append(hora.contador)
        chart['data'] = {'labels':labels,'datasets':[{'data':data, 'label':'Eventos'}]}
        charts.append(chart)

    return JsonResponse(charts,safe=False)