from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import form_login_view, form_register_view

urlpatterns = [
    path('',form_login_view,name='login'),
    path('register/',form_register_view,name='register')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)