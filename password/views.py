from django.shortcuts import render
from .models import Password
from .forms import PasswordForm

def add(request):
    form = PasswordForm(request.POST)
    if request.method == "POST":
        form = PasswordForm(request.POST)
        user = form.cleaned_data.get('Username')
        pw = form.cleaned_data.get('Password')
        TOTP = form.cleaned_data.get('TOTP')
        

# Create your views here.
