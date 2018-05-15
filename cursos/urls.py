from django.urls import path

from .views import indexCursoView, addCursoView, detailCursoView, ajaxCharts, ajaxSTDCharts, updateCursoView, \
    deleteCursoView

app_name = 'cursos'

urlpatterns = [
    path('',indexCursoView.as_view(),name='todos'),
    path('add/', addCursoView.as_view(),name="add"),
    path('<slug:slug>',detailCursoView.as_view(),name="detail"),
    path('edit/<slug:slug>',updateCursoView.as_view(),name="update"),
    path('delete/<slug:slug>',deleteCursoView.as_view(),name="delete"),
    path('ajax/',ajaxCharts,name="ajaxGeneral"),
    path('ajaxSTD/',ajaxSTDCharts,name="ajaxSTD")
]