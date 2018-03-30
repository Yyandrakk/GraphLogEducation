from random import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic

from cursos.charts import graficaTiempo, graficaTiempoSemanal, graficaTiempoHora
from cursos.models import CursoMoodle, TiempoDedicadoCursoMoodle, EstudianteCursoMoodle, \
    TiempoDedicadoEstudianteCursoMoodle
from . import models
from .forms import FormCursoMoodle


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

    def get_context_data(self, **kwargs):
        context = super(detailCursoView,self).get_context_data()
        context['estudiantes'] = EstudianteCursoMoodle.objects.filter(curso__id=context['curso'].id).order_by('nombre')
        return context

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
        # Grafica dia/#evento
        charts.append(graficaTiempo(id))
        # Grafica semana/#evento
        charts.append(graficaTiempoSemanal(id))
        # Grafica hora/#evento
        charts.append(graficaTiempoHora(id))

    return JsonResponse(charts,safe=False)

def ajaxSTDCharts(request):
    charts = []
    id = request.GET.get('id', None)
    id_std = request.GET.get('id_std', None)
    if id != None and id_std != None and EstudianteCursoMoodle.objects.filter(pk=id_std,curso_id=id).exists():
        charts.append(graficaTiempo(id,id_std))
        charts.append(graficaTiempoSemanal(id,id_std))
        charts.append(graficaTiempoHora(id,id_std))

    return JsonResponse(charts, safe=False)
