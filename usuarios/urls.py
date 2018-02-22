from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import SignUpView

app_name = 'user'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name="usuarios/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name="logout"),
    path('signup/',SignUpView.as_view(),name='signup')
]