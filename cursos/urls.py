from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import indexCursoView, addCursoView

app_name = 'cursos'

urlpatterns = [
    path('',indexCursoView.as_view(),name='todos'),
    path('add/', addCursoView.as_view(),name="add"),
]