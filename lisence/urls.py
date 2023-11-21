from django.urls import URLPattern, path
from .views import  obtain, ADobtain, TokenRequest
urlpatterns = [
    path('obtain/', obtain, name='obtain'),
    path('ADobtain/', ADobtain, name='ADobtain'),
    path('TokenRequest/', TokenRequest, name='TokenRequest'),
]