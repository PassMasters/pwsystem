from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from urllib.request import Request
from .models import Device
import base64
import os
import secrets
from pwmanager.models import Encryption, Data_ID
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# Create your views here.
n = 14595161
x = 25612561
d = 54451625
@login_required
def add(request):
   if request.method == "POST":
    device = Device()
    dID = Data_ID.objects.get(User=request.user)
    ekey = Encryption.objects.get(Owner_ID=dID.Key_lookup)
    user_id = ekey.Owner_ID
    salt = os.urandom(16)
    random = secrets.randbelow(n)
    r1 = str(random, 'UTF-8')
    r2 = bytes(r1, 'UTF-8')
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
    key = base64.urlsafe_b64encode(kdf.derive(r2))
    salt2 = bytes(ekey.Salt, 'UTF-8')
    munchy = bytes(request.POST.get('munchy'), 'UTF-8')
    kdf2 = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=300000, )
    key2 = base64.urlsafe_b64encode(kdf.derive(munchy))
    kdfmain = Fernet(key)
    key3 = bytes(key2, 'UTF-8')
    key4 = kdfmain.encrypt(key3)
    key5 = str(key4, 'UTF-8')
    device.Name = request.POST.get('name')
    device.Owner = request.user
    Cookie_UID = secrets.randbelow(x)
    UID2 = secrets.randbelow(d)
    device.DEVICE_UUID = random
    device.Salt = salt
    device.Cookie_ID = UID2
    device.Save()
    response = HttpResponse()
    response.set_cookie("UUID_device", Cookie_UID)
    response.set_cookie("UUID", UID2)
    response.set_cookie("key",key5)
    return response
   else:
     return render(request, "test.html")