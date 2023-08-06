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
import requests
from django.shortcuts import redirect

# Create your views here.
n = 14595161
x = 25612561
d = 54451625
@login_required
def add(request):
    if request.method == "POST":
     # Fetch Data_ID and Encryption objects based on request.user
        data_id = Data_ID.objects.get(User=request.user)
        encryption_key = Encryption.objects.get(Owner_ID=data_id.Key_lookup)

    # Generate random data and salts
        salt = os.urandom(16)
        salt2 = bytes(encryption_key.Salt,'UTF-8')
        random_number = secrets.randbelow(n)
        random_str = str(random_number).encode('UTF-8')

    # Derive encryption keys using PBKDF2HMAC
        kdf1 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=300000)
        key = base64.urlsafe_b64encode(kdf1.derive(random_str))

    # Fetch 'munchy' value from request and derive another encryption key
        munchy_str = request.POST.get('munchy').encode('UTF-8')
        kdf2 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt2, iterations=300000)
        key2 = base64.urlsafe_b64encode(kdf2.derive(munchy_str))

    # Encrypt 'key2' using 'key' as the encryption key
        fernet_key = Fernet(key)
        encrypted_key = fernet_key.encrypt(key2)
        encrypted_key_str = encrypted_key.decode('UTF-8')

    # Populate Device object
        device = Device()
        device.Name = request.POST.get('name')
        device.Owner = request.user
        device.DEVICE_UUID = random_number
        device.Salt = salt
        device.Cookie_ID = secrets.randbelow(d)  # Replace 'd' with your desired value for Cookie_ID

    # Save the device object
        device.save()

    # Set cookies in the response
        response = HttpResponse()
        response.set_cookie("UUID_device", str(random_number))
        response.set_cookie("UUID", str(device.Cookie_ID))
        response.set_cookie("key", encrypted_key_str)
        response.set_cookie("name", device.Name)
        return response
    else:
     return render(request, "test2.html")

def logonviadevice(request):
    if request.method == "POST":
        # Read cookies from the request
     try:
            cookie_uuid_device = request.COOKIES.get('UUID_device')
            cookie_uuid = request.COOKIES.get('UUID')
            encrypted_key_str = request.COOKIES.get('key')
            device_uuid = cookie_uuid_device
            cookie_id = cookie_uuid
            encrypted_key = bytes(encrypted_key_str, 'UTF-8')
     except Exception as e:
         return render(request, "error.html", {"message":"there was an error with your trusted device" + str(e)})
    # Convert the cookies to appropriate data types
        

    # Fetch Data_ID and Encryption objects based on the user
     data_id = Data_ID.objects.get(User=request.user)
     encryption_key = Encryption.objects.get(Owner_ID=data_id.Key_lookup)
    try:
        # Use the 'device_uuid' and 'cookie_id' to fetch the device object
        device = Device.objects.get(DEVICE_UUID=device_uuid)
        if device.Cookie_ID!= cookie_id:
            return render(request, "error2.html", {"message":"there was an error with your trusted device please clear cookies"})
        else:
            if device.Device_UUID!= device_uuid:
                return render(request, "error2.html", {"message":"there was an error with your trusted device please clear cookies"})
           
    except Exception as e:
        # Handle the case where the device with the given UUID and Cookie ID doesn't exist.
        # ...
        return render(request, "error.html", {"message": "there was an error with your trusted device"})
    # Derive the encryption key from 'munchy' using the same process as before
    munchy = device_uuid
    salt = device.Salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=300000)
    key = base64.urlsafe_b64encode(kdf.derive(munchy))

    # Decrypt the key using 'key' as the encryption key
    fernet_key = Fernet(key)
    decrypted_key = fernet_key.decrypt(encrypted_key)
    data = {"userkey": decrypted_key}
    post_url = "http://127.0.0.1:8000/passswords/trust"
    try: 
         response = requests.post(post_url, data=data)
         if response.status_code == 200:
            response2 = HttpResponse()
            response2.set_cookie("AUTH", "True")
           # POST request succeeded, redirect to the success page
            # Now perform the redirect to the desired URL
            redirect_url = "passwords/trustedview"  # Replace with the URL you want to redirect to
            return redirect(redirect_url)

         else:
            # POST request failed, handle the error or raise an exception
            # ...
            return redirect("/error/")  # Redirect to an error page or other appropriate URL

    except requests.exceptions.RequestException as e:
        # Handle exceptions, if any
        # ...
        return redirect("/error/")  # Redirect to an error page or other appropriate URL
    else:
        return render(request, "choice.html")
    # At this point, 'decrypted_key' will contain the original key used for encryption.


