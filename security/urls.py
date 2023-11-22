from django.urls import path,include
from . import views
from django.views.generic import TemplateView
urlpatterns = [
  path('munchy', views.TrustedDeviceInit),
  path('cookie', views.CookieCheck),
  path('userkey', views.encryptuserkey)
]