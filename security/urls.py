from django.urls import path,include
from . import views
from django.views.generic import TemplateView
urlpatterns = [
  path('test', TemplateView.as_view(template_name="test2.html")),
  path('add', views.add)
]