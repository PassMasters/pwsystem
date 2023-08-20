#import re
# da terminal not shared how is someone supposed to see it or how i run the code/runserver

import re
from django.contrib.auth.models import User
from urllib.request import Request
from django.shortcuts import render, get_object_or_404
from .models import PW, Encryption, Data_ID
from .forms import PwEdit
from datetime import date
import base64
import os
import json
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.shortcuts import redirect
from django.http import HttpResponse
from cryptography.fernet import Fernet
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
import json
import pyotp
import time
from security import crypt
def digitcheck(number, len2):
    return len(str(number)) == len2
n = 9999999999
@login_required
def setup(request):
    if request.method == "POST":
        ekey = Encryption()
        dID = Data_ID()
        password = bytes(request.POST.get('munchy'), 'UTF-8')
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        ekey.Owner = request.user
        num2 = secrets.randbelow(n)
        if digitcheck(num2, 10) == True:
            ekey.Owner_ID = num2
            dID.Key_lookup = num2
            dID.User = request.user
            dID.save()
        else: 
            return redirect('/error')
        ekey.Salt = salt
        ekey.save() 
        return redirect('/')
    else:
        return render(request, "test.html")
        
@login_required
def add(request):
    if request.method == "POST":
        dID = Data_ID.objects.get(User=request.user)
        ekey = Encryption.objects.get(Owner_ID=dID.Key_lookup)
        user_id = ekey.Owner_ID
        s = PW()
        salt = bytes(ekey.Salt, 'UTF-8')
        munchy = bytes(request.POST.get('munchy'), 'UTF-8')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
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

def homepage(request):
    if request.method == 'POST':
        passwordss = PW.objects.filter(Owner=request.user).values('Password', 'Username')
        totpmunchy = PW.objects.filter(Owner=request.user).values('TOTP')
        PKS = list(PW.objects.filter(Owner=request.user).values('pk'))
        ekey = Encryption.objects.get(Owner=request.user)
        salt = bytes(ekey.Salt,'UTF-8')
        pin = bytes(request.POST.get('munchy'), 'UTF-8')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
        key = base64.urlsafe_b64encode(kdf.derive(pin))
        ks = Fernet(key)
        mainlist = []
        munchylist = list(totpmunchy)
        y = list(passwordss)
        for i in range(len(y)):
            y1 = dict(y[i])
            y2 = y1['Username']
            y3 = bytes(y1['Password'], 'UTF-8')
            y5 = ks.decrypt(y3)
            y6 = str(y5, 'UTF-8')
        
            x1 = munchylist[i]
            x3 = json.dumps(x1)
            x4 = json.loads(x3)
            x5 = x4['TOTP']
            x6 = bytes(x5, 'UTF-8')
            x8 = ks.decrypt(x6)
            x7 = str(x8, 'UTF-8')
            totp = pyotp.TOTP(x7)
            x9 = totp.now()
        
            z = PKS[i]
            z1 = z['pk']
            z2 = PW.objects.get(pk=z1)
            z3 = z2.get_absolute_url()
        
            data_dict = {
                "Username": y2,
                "Password": y6,
                "TOTP": x9,
                "EditURL": z3
            }
        
            mainlist.append(data_dict)
        return render (request, 'pw_homepage.html', {'munchy': mainlist})
    else:
         return render(request, 'pin.html')




def Edit(request, pk):
    pw = get_object_or_404(PW, pk=pk)
    ekey = Encryption.objects.get(Owner=request.user)
    salt = bytes(ekey.Salt,'UTF-8')
    if request.method == 'POST':
       pin = bytes(request.POST.get('munchy'), 'UTF-8')
       kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
       key = base64.urlsafe_b64encode(kdf.derive(pin))
       form = PwEdit(request.POST, request.FILES, instance=pw)
       if form.is_valid():
            form.save()
            pw.Password = crypt.encrypt(form.cleaned_data.get('Password'), key)
            pw.Password = crypt.encrypt(form.cleaned_data.get('TOTP'), key)
            pw.save()
            return redirect('/')
    else:
        if request.method =='GET':
            try:
                data = request.GET.get("munchy")
                pin = bytes(data, 'UTF-8')
                kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
                key = base64.urlsafe_b64encode(kdf.derive(pin))
                form_initial = crypt.decrypt(pw, key)
                form = PwEdit(instance=pw, initial=form_initial)
                return render(request, 'form.html', {'form': form})
            except Exception as e:
                return render(request, 'pinget.html')
def Destory(request, pk):
    pw = get_object_or_404(PW, pk=pk)
    if request.method == 'POST':
        if pw.Owner == request.user:
            pw.delete()
            return redirect('/')
        else:
             return render(request, 'error.html')
    else:
        return render(request, "delete.html")

def deleteAccount(request):
    if request.method == 'POST':
        dID = Data_ID.objects.get(User=request.user)
        ekey = Encryption.objects.get(Owner_ID=dID.Key_lookup)
        dID.delete()
        ekey.delete()
        user = User.objects.get(username=request.user)
        user.delete()
        return redirect('/')
    else:
        return render(request, 'accountd.html')