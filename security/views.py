from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from urllib.request import Request
from .models import Device, UserServerKeys
import base64
import os
import secrets
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
        response = HttpResponse("munchy")
        response.set_cookie('privatekey', deviceprivate, secure=True)
        devicepublic = devicekeypair.publickey().export_key()
        response.set_cookie('public', devicepublic, secure=True)
        name = "munchy"
        user = request.user
        model = Device()
        model.Name = name
        model.Owner = user
        model.Pub_key = devicepublic
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