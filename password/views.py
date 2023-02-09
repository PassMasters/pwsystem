from django.shortcuts import render
from .models import Password, Encryption
from .forms import PasswordForm, KeyForm
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse
from cryptography.fernet import Fernet

def setup(request):
    if request.method == "POST":
        ekey = Encryption()

        ekey.Owner = request.user
        ekey.save() 

        return redirect('/')

        


def add(request):
    form = PasswordForm(request.POST)
    if request.method == "POST":
        
        ekey = Encryption()
        


        form = PasswordForm(request.POST)
        user = form.cleaned_data.get('Username')
        pw = form.cleaned_data.get('Password')
        TOTP = form.cleaned_data.get('TOTP')
        Atachment = form.cleaned_data('Atachment')
        

           
        return redirect('')

# Create your views here.
