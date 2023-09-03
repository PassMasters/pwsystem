#import re
# da terminal not shared how is someone supposed to see it or how i run the code/runserver


from django.contrib.auth.models import User
from urllib.request import Request
from django.shortcuts import render, get_object_or_404
from .models import PW, Encryption, Data_ID, PWcheck
from .forms import PwEdit
from datetime import date
import base64
import os
import json
import secrets
from django.shortcuts import redirect
import bcrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
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
        PWcheck2 = PWcheck()
        password = bytes(request.POST.get('pin'), 'UTF-8')
        if len(password) > 5:
            # genrate salt and inilzation vector
            salt = os.urandom(16)
            iv = os.urandom(16)
            #derive key and init AES
            encryption_key = bcrypt.kdf(password, salt,rounds=24,  desired_key_bytes=32,)
            keys = AES.new(encryption_key, AES.MODE_CBC, iv)
            #genrate a pwcheck entry 
            test = secrets.randbelow(n)
            testpw = test.to_bytes(8, byteorder='big')
            padlen = 16 -(len(testpw) % 16)
            padded = testpw + bytes([padlen]) * padlen
            encrypted = keys.encrypt(padded)
            ekey.Owner = request.user
            PWcheck2.Owner = request.user
            PWcheck2.Test_PW = encrypted
            PWcheck2.Answer = test
            num2 = secrets.randbelow(n)
            PWcheck2.Owner_ID = num2
            #saving 
            ekey.Owner_ID = num2
            ekey.IV = iv
            dID.Key_lookup = num2
            dID.User = request.user
            dID.save()
            PWcheck2.save()
            ekey.Salt = salt
            ekey.save()
        else:
            return redirect('passwords/error')
         
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
        iv = bytes(ekey.IV, 'UTF-8')
        print(iv)
        print(len(iv))
        iv2 = eval(iv)
        print(iv2)
        iv = iv2
        pin = bytes(request.POST.get('pin'),'UTF-8')
        encryption_key = bcrypt.kdf(pin, salt, rounds=24,  desired_key_bytes=32)
        keys = AES.new(encryption_key, AES.MODE_CBC, iv)
        check = crypt.check(request.user, encryption_key)
        if check != True:
            return render(request, 'error.html')
        user = request.POST['username']
        pw = request.POST['Password']
        pw2 = bytes(pw, 'UTF-8')
        paded = 16 - (len(pw2) % 16)
        padded_text += bytes([paded]) * paded
        newPassword = keys.encrypt(padded_text)
        newPassword2 = str(newPassword,'UTF-8')
        pw = newPassword2
        TOTP = request.POST['TOTP']
        if TOTP == "":
            T2 = ""
            newTOTP2 = T2
        else:
            
            T2 = bytes(TOTP, 'UTF-8')
            padingTOTP = 16 - (len(T2) % 16)
            padded_TOTP += bytes([paded]) * paded
            newTOTP = keys.encrypt(padded_TOTP)
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
    
@login_required
def homepage(request):
    if request.method == 'POST':
        passwordss = PW.objects.filter(Owner=request.user).values('Password', 'Username')
        totpobj = PW.objects.filter(Owner=request.user).values('TOTP')
        URI = list(PW.objects.filter(Owner=request.user).values('URL', 'Notes'))
        PKS = list(PW.objects.filter(Owner=request.user).values('pk'))
        ekey = Encryption.objects.get(Owner=request.user)
        salt = bytes(ekey.Salt,'UTF-8')
        iv = bytes(ekey.IV, 'UTF-8')
        print(iv)
        print(len(iv))
        iv2 = eval(iv)
        print(iv2)
        iv = iv2
        pin = bytes(request.POST.get('pin'), 'UTF-8')
        encryption_key = bcrypt.kdf(pin, salt,rounds=24,  desired_key_bytes=32)
        keys = AES.new(encryption_key, AES.MODE_CBC, iv)
        check = crypt.check(request.user, encryption_key)
        if check != True:
            return render(request, 'error.html')
        mainlist = []
        totplist = list(totpobj)
        pwlist = list(passwordss)
        try:
            for i in range(len(pwlist)):

                y1 = dict(pwlist[i])
                y2 = y1['Username']
                y3 = bytes(y1['Password'], 'UTF-8')

                y5 = keys.decrypt(y3)
                padding_length1 = y5[-1]
                plaintext_bytes1 = y5[:-padding_length1]

                y6 = str(plaintext_bytes1, 'UTF-8')
        
                x1 = totplist[i]
                x3 = json.dumps(x1)
                x4 = json.loads(x3)
                x5 = x4['TOTP']
                if x5 == "":
                    x9 = "N/A"
                else:
                    x6 = bytes(x5, 'UTF-8')
                    x8 = keys.decrypt(x6)
                    padding_length2 = x8[-1]
                    plaintext_bytes2 = x8[:-padding_length2]
                    x7 = str(x8, 'UTF-8')
                    totp = pyotp.TOTP(x7)
                    x9 = totp.now()
                z = PKS[i]
                z1 = z['pk']
                z2 = PW.objects.get(pk=z1)
                z3 = z2.get_absolute_url()
                notes = URI[i]
                notes1 = notes['Notes']
                url = URI[i]
                url1 = url['URL']
                data_dict = {
                "Username": y2,
                "Password": y6,
                "TOTP": x9,
                "URL" : url1,
                "notes" : notes1,
                "EditURL": z3
            }
        
                mainlist.append(data_dict)
                return render (request, 'pw_homepage.html', {'pwlist': mainlist})
        except Exception as e:
            msg ="an error has occured decypting passwords"
            return render(request, 'error.html', {'msg': msg })
    else:
         return render(request, 'pin.html')



@login_required
def Edit(request, pk):
    pw = get_object_or_404(PW, pk=pk)
    ekey = Encryption.objects.get(Owner=request.user)
    salt = bytes(ekey.Salt,'UTF-8')
    if request.method == 'POST':
       pin = bytes(request.POST.get('pin'), 'UTF-8')
       key = bcrypt.kdf(pin, salt, rounds=24, desired_key_bytes=32)
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
                data = request.GET.get("pin")
                pin = bytes(data, 'UTF-8')
                key = bcrypt.kdf(pin, salt, desired_key_bytes=32)
                form_initial = crypt.decrypt(pw, key)
                form = PwEdit(instance=pw, initial=form_initial)
                return render(request, 'form.html', {'form': form})
            except Exception as e:
                return render(request, 'pinget.html')
@login_required
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
@login_required
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

