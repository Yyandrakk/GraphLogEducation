from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic

from cursos.charts import graficaTiempo, graficaTiempoSemanal, graficaTiempoHora, graficaTiempoMedioContexto, \
    graficaTiempoInvertido, graficaUsoArchivos
from cursos.models import CursoMoodle, EstudianteCursoMoodle
from . import models
from .forms import FormCursoMoodle, FormUpdateCMoodle, ConfirmDeleteForm


def unique_slug_generator(slug):
    if CursoMoodle.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{rand}".format(
            slug=slug,
            rand=randint(0, 1000)
        )
        return unique_slug_generator(slug=new_slug)
    return slug


class indexCursoView(LoginRequiredMixin, generic.ListView):
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
        self.object = form.save(commit=False)
        self.object.profesor = self.request.user
        self.object.slug = unique_slug_generator(slugify(self.object.nombre))
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(addCursoView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


class detailCursoView(LoginRequiredMixin, generic.DetailView):
    template_name = "cursos/detailCurso.html"
    model = models.CursoMoodle
    context_object_name = 'curso'

    def get_context_data(self, **kwargs):
        context = super(detailCursoView, self).get_context_data()
        curso = context['curso']
        context['estudiantes'] = EstudianteCursoMoodle.objects.filter(curso__id=curso.id).order_by('nombre')
        context['otrosCursos'] = CursoMoodle.objects.exclude(id=curso.id).exclude(procesado=False) \
            .filter(profesor__id=curso.profesor_id).order_by('nombre')
        return context

    def user_test(self, request, slug):
        return models.CursoMoodle.objects.filter(slug=slug, profesor_id=request.user.id).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.user_test(request, kwargs.get('slug', '')):
            return redirect("cursos:todos")
        return super().dispatch(
            request, *args, **kwargs)


class deleteCursoView(LoginRequiredMixin, generic.DeleteView):
    template_name = "cursos/deleteCurso.html"
    model = models.CursoMoodle
    success_url = reverse_lazy("cursos:todos")
    form_class = ConfirmDeleteForm
    context_object_name = 'curso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            context['form'] = ConfirmDeleteForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConfirmDeleteForm(request.POST, instance=self.object)

        if form.is_valid():
            return self.delete(request, *args, **kwargs)
        else:
            return self.render_to_response(
                self.get_context_data(form=form),
            )

    def user_test(self, request, slug):
        return models.CursoMoodle.objects.filter(slug=slug, profesor_id=request.user.id).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.user_test(request, kwargs.get('slug', '')):
            return redirect("cursos:todos")
        return super().dispatch(
            request, *args, **kwargs)


class updateCursoView(LoginRequiredMixin, generic.UpdateView):
    template_name = "cursos/updateCurso.html"
    model = models.CursoMoodle
    form_class = FormUpdateCMoodle
    context_object_name = 'curso'
    success_url = reverse_lazy("cursos:todos")

    def get_initial(self):
        initial = super(updateCursoView, self).get_initial()
        initial['desc'] = self.object.desc
        initial['umbral'] = self.object.umbral
        return initial

    def form_valid(self, form):
        if (form.has_changed() and form.is_valid()):
            form.instance = CursoMoodle.objects.get(id=self.object.id)
            form.save(commit=True)

        return HttpResponseRedirect(self.get_success_url())

    def user_test(self, request, slug):
        return models.CursoMoodle.objects.filter(slug=slug, profesor_id=request.user.id).exists()

    def get_context_data(self, **kwargs):
        context = super(updateCursoView, self).get_context_data()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.user_test(request, kwargs.get('slug', '')):
            return redirect("cursos:todos")
        return super().dispatch(
            request, *args, **kwargs)



def ajaxCharts(request):
    if not request.user.is_authenticated:
        jsonr = {'authenticated': False}
        return JsonResponse(jsonr, safe=False)

    charts = []
    id = request.GET.get('id', None)
    idsGN = request.GET.get('idsGN', None)
    if id != None and CursoMoodle.objects.filter(pk=id,profesor_id=request.user.id).exists():
        # Grafica dia/#evento
        charts.append(graficaTiempo(id, idsGN=idsGN))
        # Grafica semana/#evento
        charts.append(graficaTiempoSemanal(id, idsGN=idsGN))
        # Grafica hora/#evento
        charts.append(graficaTiempoHora(id))
        # Grafica media contextos
        charts.append(graficaTiempoMedioContexto(id))
        # Grafica tiempo invertido
        charts.append(graficaTiempoInvertido(id))
        #Grafica de uso de archivos
        charts.append(graficaUsoArchivos(id))


    return JsonResponse(charts, safe=False)


def ajaxSTDCharts(request):
    if not request.user.is_authenticated:
        jsonr = {'authenticated': False}
        return JsonResponse(jsonr,safe=False)

    charts = []
    id = request.GET.get('id', None)
    id_std = request.GET.get('id_std', None)
    if id != None and id_std != None and CursoMoodle.objects.filter(pk=id,profesor_id=request.user.id).exists() and EstudianteCursoMoodle.objects.filter(pk=id_std, curso_id=id).exists():
        charts.append(graficaTiempo(id, id_std))
        charts.append(graficaTiempoSemanal(id, id_std))
        charts.append(graficaTiempoHora(id, id_std))
        charts.append(graficaTiempoMedioContexto(id, id_std))
        charts.append(graficaTiempoInvertido(id, id_std))

    return JsonResponse(charts, safe=False)
