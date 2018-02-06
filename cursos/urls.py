from django.urls import path
from .views import indexCursoView, addCursoView, detailCursoView

app_name = 'cursos'

urlpatterns = [
    path('',indexCursoView.as_view(),name='todos'),
    path('add/', addCursoView.as_view(),name="add"),
    path('<slug:slug>',detailCursoView.as_view(),name="detail")
]