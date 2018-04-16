from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic

from cursos.charts import graficaTiempo, graficaTiempoSemanal, graficaTiempoHora, graficaTiempoMedioContexto
from cursos.models import CursoMoodle, EstudianteCursoMoodle
from . import models
from .forms import FormCursoMoodle, FormUpdateCMoodle


def unique_slug_generator(slug):

    if CursoMoodle.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{rand}".format(
            slug=slug,
            rand=randint(0,1000)
        )
        return unique_slug_generator(slug=new_slug)
    return slug

class indexCursoView(LoginRequiredMixin,generic.ListView):
    template_name = "cursos/listCursos.html"
    context_object_name = 'curso_list'
    models = models.CursoMoodle

    def get_queryset(self):
        return self.models.objects.filter(profesor_id=self.request.user.id)


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
        curso = context['curso']
        context['estudiantes'] = EstudianteCursoMoodle.objects.filter(curso__id=curso.id).order_by('nombre')
        context['otrosCursos'] = CursoMoodle.objects.exclude(id=curso.id).exclude(procesado=False).filter(profesor__id=curso.profesor_id).order_by('nombre')
        return context

    def user_test(self,request,slug):
        return models.CursoMoodle.objects.filter(slug=slug,profesor_id=request.user.id).exists()


    def dispatch(self, request, *args, **kwargs):
        if not self.user_test(request,kwargs.get('slug','')):
            return redirect("cursos:todos")
        return super().dispatch(
            request, *args, **kwargs)


class updateCursoView(LoginRequiredMixin, generic.UpdateView):
    template_name = "cursos/updateCurso.html"
    model = models.CursoMoodle
    form_class = FormUpdateCMoodle
    context_object_name = 'curso'
    success_url = reverse_lazy("cursos:todos")

    def user_test(self,request,slug):
        return models.CursoMoodle.objects.filter(slug=slug,profesor_id=request.user.id).exists()

    def get_context_data(self, **kwargs):
        context = super(updateCursoView,self).get_context_data()
        return context

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
    idsGN = request.GET.get('idsGN', None)
    if id != None and CursoMoodle.objects.filter(pk=id).exists():
        # Grafica dia/#evento
        charts.append(graficaTiempo(id,idsGN=idsGN))
        # Grafica semana/#evento
        charts.append(graficaTiempoSemanal(id,idsGN=idsGN))
        # Grafica hora/#evento
        charts.append(graficaTiempoHora(id))
        # Grafica media contextos
        charts.append(graficaTiempoMedioContexto(id))
    return JsonResponse(charts,safe=False)

def ajaxSTDCharts(request):
    charts = []
    id = request.GET.get('id', None)
    id_std = request.GET.get('id_std', None)
    if id != None and id_std != None and EstudianteCursoMoodle.objects.filter(pk=id_std,curso_id=id).exists():
        charts.append(graficaTiempo(id,id_std))
        charts.append(graficaTiempoSemanal(id,id_std))
        charts.append(graficaTiempoHora(id,id_std))
        charts.append(graficaTiempoMedioContexto(id,id_std))

    return JsonResponse(charts, safe=False)
