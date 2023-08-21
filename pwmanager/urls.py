from os import name
from django.urls import path,include
#from accounts.views import profile,login1,transaction
#from .views import profile
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
   
   path("add2", views.add, name='sdf'),
   path('setup',views.setup, name='keysetuptest'),
   path('test',TemplateView.as_view(template_name="test.html")),
   path('add',TemplateView.as_view(template_name="pwtest.html")),
   path('munchy', views.homepage, name='munchy'),
   path('error', TemplateView.as_view(template_name="error.html")),
   path('edit/<int:pk>/', views.Edit, name='edit'),
   path('delete/<int:pk>/', views.Destory, name='delete'),
   path('destroyaccount', views.deleteAccount),
]
