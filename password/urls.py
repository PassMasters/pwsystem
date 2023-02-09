from django.urls import path,include
#from accounts.views import profile,login1,transaction
#from .views import profile
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
   path("add", views.PasswordForm, name='sdf'),
   path('setup',views.setup, name='keysetuptest'),
   path('test',TemplateView.as_view(template_name="test.html")),
]
