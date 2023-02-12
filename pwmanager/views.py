from django.shortcuts import render
from .models import Password, Encryption
from .forms import PasswordForm, KeyForm
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse
from cryptography.fernet import Fernet
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import model_to_dict
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
@login_required
def decrypt2(request, pk):
    if request.method =="POST":
        ekey = Encryption.objects.get(Owner=request.user)
        
        salt = bytes(ekey.Salt, 'UTF-8')
        munchy = bytes(request.POST.get('munchy'), 'UTF-8')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=100000, )
        key = base64.urlsafe_b64encode(kdf.derive(munchy))
        user_id = ekey.Id
        ks = Fernet(key)
        pw = Password.objects.filter(pk=pk).values('Password')
        pw2 = list(pw)
        pw3 = pw2.__getitem__(0)
        str2 = json.dumps(pw3)
        resp = json.loads(str2)
        pw9 = resp['Password']
    
        y2 = bytes(pw9, 'UTF-8')
        y3 = ks.decrypt(y2)
        y4 = str(y3, 'UTF-8')
        print(y4)

        return HttpResponse(y4)
    else:
        return render(request, "pin.html")
@login_required
def decrypt(request):
    if request.method == "GET":
        ekey = Encryption.objects.get(Owner=request.user)
        token = ekey.Key
        user_id = ekey.Id
        ks = Fernet(token)
        a = Password.objects.filter(Id=user_id)
       
        
        return HttpResponse(a)


@login_required
def setup(request):
    if request.method == "POST":
        ekey = Encryption()
        password = bytes(request.POST.get('munchy'), 'UTF-8')
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=100000, )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        ekey.Owner = request.user
        ekey.Id = request.POST.get('munchy')
        ekey.Salt = salt
        ekey.save() 

        return redirect('/')
    else:
        return render(request, "test.html")
        

@login_required
def add(request):
    
    if request.method == "POST":
        
        ekey = Encryption.objects.get(Owner=request.user)
       
        user_id = ekey.Id
        s = Password()
        
        salt = bytes(ekey.Salt, 'UTF-8')
        
        munchy = bytes(request.POST.get('munchy'), 'UTF-8')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=100000, )
        key = base64.urlsafe_b64encode(kdf.derive(munchy))
        ks = Fernet(key)
        user = request.POST['username']
        pw = request.POST['Password']
        pw2 = bytes(pw, 'UTF-8')
        newPassword = ks.encrypt(pw2)
        newPassword2 = str(newPassword,'UTF-8')
        pw = newPassword2
        TOTP = request.POST['TOTP']
        T2 = bytes(TOTP, 'UTF-8')
        newTOTP = ks.encrypt(T2)
        newTOTP2 = str(newTOTP, 'UTF-8')
        TOTP = newTOTP2
        Atachment = request.POST['File']
        Date = request.POST['date']
        Owner = request.user
        s.Username = user
        s.Password = newPassword2
        s.TOTP = newTOTP2
        s.Atachment = Atachment
        s.Date_Created = Date
        s.Owner = Owner
        s.Id = user_id
        s.save()
        
           
        return redirect('/')

# Create your views here.
