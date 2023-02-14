
from urllib.request import Request
from django.shortcuts import render
from .models import Password, Encryption
from .crypt import encrypt, decrypt
from datetime import date
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.shortcuts import redirect
from django.http import HttpResponse
from cryptography.fernet import Fernet
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .crypt import decrypt 
import json

@login_required
def decrypt2(request, pk):
    if request.method =="POST":
        ekey = Encryption.objects.get(Owner=request.user)
        
        salt = ekey.Salt
        munchy = bytes(request.POST.get('munchy'), 'UTF-8')
        pw = Password.objects.filter(pk=pk).values('Password')
        pw2 = dict(pw)
        pw3 = bytes(pw2['Password'], 'UTF-8')
    #decryption system does not work 
    
        y3 = decrypt(munchy, pw3, salt)
        
        print(y3)

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

def homepage(request):
    if request.method == 'POST':
   # Encryptions = Encryption.objects.all()
   # ekey = Encryption.objects.get(Owner=request.user)
   #passwords = Password.objects.all()#(Owner=request.user
        passwordss = Password.objects.filter(Owner=request.user).values('Password', 'Username')
        totpmunchy = Password.objects.filter(Owner=request.user).values('TOTP')
        ekey = Encryption.objects.get(Owner=request.user)
        salt = bytes(ekey.Salt,'UTF-8')
        pin = bytes(request.POST.get('munchy'), 'UTF-8')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=100000, )
        key = base64.urlsafe_b64encode(kdf.derive(pin))
        ks = Fernet(key)
        mainlist = []
        munchylist = list(totpmunchy)
        for i in range(len(munchylist)):
            x1  = munchylist[i]
            x3 = json.dumps(x1)
            x4 = json.loads(x3)
            print(x3)
            x5 = x4['TOTP']
            x6 = bytes(x5, 'UTF-8')
            x8 = ks.decrypt(x6)
            x7 = str(x8, 'UTF-8')

            mainlist.append(x7)
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
            mainlist.append(y2)
            mainlist.append(y6)
           

        return render (request, 'pw_homepage.html', {'munchy': mainlist})

    else:
         return render(request, 'pin.html')


# Create your views here.
