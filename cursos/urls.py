from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import indexCursoView

app_name = 'cursos'

urlpatterns = [
    path('',indexCursoView.as_view(),name='todos'),
    path('logout/', auth_views.LogoutView.as_view(),name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)