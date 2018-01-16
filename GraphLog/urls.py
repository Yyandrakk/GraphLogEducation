from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

app_name = 'graph'

urlpatterns = [
  path('',TemplateView.as_view(template_name="GraphLog/index.html"),name='index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)