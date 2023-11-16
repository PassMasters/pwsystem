from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from urllib.request import Request
from .models import Device, UserServerKeys
from pwmanager.models import PW
import base64
import os
import secrets
import bcrypt
from pwmanager.models import Encryption, Data_ID
import cryptography
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import requests
from django.shortcuts import redirect
from django.conf import settings
BASE_DIR = settings.BASE_DIR
# Create your views here.
n = 14595161
x = 25612561
d = 54451625
def TrustedDeviceInit(request):
    if request.method!="GET":
        devicekeypair = RSA.generate(2048)
        print(devicekeypair)
        deviceprivate = devicekeypair.export_key()
        serverpublic = open(os.path.join(BASE_DIR, 'public.pem')).read()
        response = HttpResponse("munchy")
        response.set_cookie('privatekey', deviceprivate, secure=True)
        devicepublic = devicekeypair.publickey().export_key()
        response.set_cookie('public', devicepublic, secure=True)
        response.set_cookie('serverpublic', serverpublic, secure=True)
        name = request.POST.get('name')
        user = request.user
        uuid = secrets.randbelow(d)
        model = Device()
        model.Name = name
        model.Owner = user
        model.Pub_key = devicepublic
        model.uid = uuid
        model.save()
        return response
    else:
        return render(request, "postinit.html")
def CookieCheck(request):
    public = request.COOKIES.get('public')
    private = request.COOKIES.get('privatekey')
    return HttpResponse(public + private)
def encryptuserkey(request):
    public = bytes(request.COOKIES.get('public'), 'UTF-8')
    key = os.urandom(16)
    server_private = RSA.import_key(open(os.path.join(BASE_DIR, 'private.pem')).read())
    key_str = public.decode('utf-8')
    key_str = key_str.replace("b'", "").replace("'", "").replace("\\n", "\n").strip()
    device_public_key = RSA.import_key(key_str)
    cipher_device = PKCS1_OAEP.new(device_public_key)
    encrypted_key_for_device = cipher_device.encrypt(key)
    response = HttpResponse("key provisioned successfully")
    response.set_cookie('Userkey', encrypted_key_for_device)
    cipher_server = PKCS1_OAEP.new(server_private)
    encrypted_key_for_server = cipher_server.encrypt(key)
    model = UserServerKeys()
    model.Owner = request.user
    model.key = encrypted_key_for_server
    model.save()
    return response
def Destroykeys(request):
    if request.method =="POST":
        key = request.post.get('privatekey')
        server = open(os.path.join(BASE_DIR, 'private.pem')).read()
        if key == server:
            munchy = UserServerKeys()
            munchy.objects.all().delete()
        else:
            rsponse = HttpResponse("SECURITY BREACH")
            return rsponse    
    else:
        return render(request, 'selfdestruct.html')
def removedevice(request):
    dev = Device()
    user = request.user
    response = HttpResponse("deviceremoved")
    public = response.COOKIES.get('public')
    obj = dev.objects.get(pk=public)
    if obj.Owner == user:
        obj.delete()
        return response
    else: 
        response.delete_cookie('public')
        return response
def autologonsetup(request):
    user = request.user
    dev = Device()
    server_private = RSA.import_key(open(os.path.join(BASE_DIR, 'private.pem')).read())
    if request.method =='POST':
        dID = Data_ID.objects.get(User=request.user)
        ekey = Encryption.objects.get(Owner_ID=dID.Key_lookup)
        user_id = ekey.Owner_ID
        s = PW()
        salt = bytes(ekey.Salt, 'UTF-8')
        iv = bytes(ekey.IV, 'UTF-8')
        iv2 = eval(iv)
        iv = iv2
        pin = bytes(request.POST.get('pin'),'UTF-8')
        encryption_key = bcrypt.kdf(pin, salt, rounds=24,  desired_key_bytes=32)
        public = bytes(request.COOKIES.get('public'), 'UTF-8')    
        key_str = public.decode('utf-8')
        key_str = key_str.replace("b'", "").replace("'", "").replace("\\n", "\n").strip()
        device_public_key = RSA.import_key(key_str)
        cipher_device = PKCS1_OAEP.new(device_public_key)
        cipher_server = PKCS1_OAEP.new(server_private)
        devicekey = cipher_device.encrypt(encryption_key)
        response = HttpResponse("devices setup sucessful")
        response.set_cookie('encryptedmessage', "MUNCHY")
        response.set_cookie('autologonkey', devicekey)
        return response
    else:
        return render(request, 'autologonsetup.html')
