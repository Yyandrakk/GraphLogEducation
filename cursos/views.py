from random import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import ExtractWeek
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic

from cursos.models import CursoMoodle, TiempoDedicadoCursoMoodle, EstudianteCursoMoodle
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
        dias = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id,tipo=TiempoDedicadoCursoMoodle.DIA)
        count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id,tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(total=Sum('contador'))
        chart = {'type': 'line'}
        labels = []
        data = []
        for dia in dias:
            labels.append(format(dia.timestamp,"%d/%m/%Y"))
            data.append((dia.contador/count['total'])*100)
        chart['data'] = {'labels':labels,'datasets':[{'data':data,'borderColor': "#3e95cd", 'label':'Eventos'}]}
        charts.append(chart)

        # Grafica semana/#evento
        chart = {'type': 'line'}
        labels = []
        data = []
        semanas =  TiempoDedicadoCursoMoodle.objects.filter(curso_id=id,tipo=TiempoDedicadoCursoMoodle.DIA).annotate(week=ExtractWeek('timestamp')).values('week').annotate(s=Sum('contador')).values('week', 's').order_by('week')
        for semana in semanas:
            labels.append(semana['week'])
            data.append((semana['s'] / count['total']) * 100)
        chart['data'] = {'labels': labels, 'datasets': [{'data': data, 'borderColor': "#3e95cd", 'label': 'Eventos'}]}
        charts.append(chart)
        # Grafica hora/#evento
        chart = {'type': 'bar'}
        labels = []
        data = []
        horas = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id, tipo=TiempoDedicadoCursoMoodle.HORA)
        count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id, tipo=TiempoDedicadoCursoMoodle.HORA).aggregate(total=Sum('contador'))
        for hora in horas:
            labels.append(format(hora.timestamp,"%H"))
            data.append((hora.contador/count['total'])*100)

        chart['data'] = {'labels':labels,'datasets':[{'data':data,'backgroundColor': ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#C4A73D","#7EC44A","#C44148","#C4249F", "#110EC4","#AF19FF","#18FFDD","#FFD558","#3e96cd", "#5e5ea2","#3c3a9f","#e823b9","#c45810","#CAA73D","#7E444A","#C43148","#C4219F", "#113EC4","#AF29FF","#18FFAD"], 'label':'Eventos'}]}
        charts.append(chart)

    return JsonResponse(charts,safe=False)

def ajaxSTDCharts(request):
    charts = []
    id = request.GET.get('id', None)
    id_std =  request.GET.get('id_std', None)