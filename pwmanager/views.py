from urllib.request import Request
from django.shortcuts import render
from .models import PW, Encryption
from datetime import date
import base64
import os
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
def digitcheck(number, len2):
    return len(str(number)) == len2
n = 9999999999
@login_required
def setup(request):
    if request.method == "POST":
        ekey = Encryption()
        password = bytes(request.POST.get('munchy'), 'UTF-8')
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        ekey.Owner = request.user
        num2 = secrets.randbelow(n)
        if digitcheck(num2, 10) == True:
            ekey.ID = num2
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
        ekey = Encryption.objects.get(Owner=request.user)
        user_id = ekey.Id
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
            y7  = y[i]
            y1 = dict(y7)
            y2 = y1['Username']
            print(y2)
            y3 = bytes(y1['Password'], 'UTF-8')
            y5 = ks.decrypt(y3)
            y6 = str(y5, 'UTF-8')
            print(y3)
            print(y5)
            mainlist.append("Useraname:")
            mainlist.append(y2)
            mainlist.append("Password:")
            mainlist.append(y6)
            x1  = munchylist[i]
            x3 = json.dumps(x1)
            x4 = json.loads(x3)
            print(x3)
            x5 = x4['TOTP']
            x6 = bytes(x5, 'UTF-8')
            x8 = ks.decrypt(x6)
            x7 = str(x8, 'UTF-8')
          
            totp = pyotp.TOTP(x7)
            x9 = totp.now()
            mainlist.append("TOTP:")
            mainlist.append(x9)
        return render (request, 'pw_homepage.html', {'munchy': mainlist})
    else:
         return render(request, 'pin.html')
