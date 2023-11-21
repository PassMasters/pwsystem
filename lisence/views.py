import json
from django.shortcuts import render
from . import models

import uuid
from django.http import JsonResponse
from django.shortcuts import redirect

import jwt
from Crypto.PublicKey import RSA
import secrets
import hashlib
from datetime import datetime, timedelta
# Create your views here.

def obtain(request):
    if request.method != 'POST':
        return render(request, 'lisence/index.html')
    else:
        #gen uuid
        model = models.lisence()
        username = request.user.username
        model.name = request.POST.get('name')
        model.key = uuid.uuid4()
        model.Type = "User(not AD)"
        model.Activations = 0
        model.Limit = 1
        model.save()
        context = {'generated_uuid': str(model.key)}
        return render(request, 'lisence/key.html', context)
    
def ADobtain(request):
    if request.method != 'GET':
        return render(request, 'lisence/index.html')
    else:
        #gen uuid
        model = models.lisence()
        username = request.user.username
        if "cs4265" in username:
            model.name = request.post.get('name')
            model.key = uuid.uuid4()
            model.Type = "AD User"
            model.Activations = 0
            model.Limit = 80
            model.save()
            context = {'generated_uuid': str(model.key)}
            return render(request, 'lisence/key.html', context)
        else:
            return redirect('http://10.10.0.5')
        



def TokenRequest(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'})
    else: 
        token = request.POST.get('key')
        model = models.lisence()
        try:
            model = models.lisence.objects.get(key=token)
        except models.lisence.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=403)
        if model.Type == "AD User":
            #internal server
            return redirect('http://10.10.0.5')
        model.Activations = model.Activations + 1
        if model.Activations > model.Limit:
            return JsonResponse({'error': 'limit reached'}, status=403)
        model.save()
        random_number = secrets.randbelow(454156146614)
        my_uuid = token
        combined_data = f"{random_number}{my_uuid}"
        hashed_data = hashlib.sha256(combined_data.encode()).hexdigest()
        expiration_time = datetime.utcnow() + timedelta(days=30)
        secret = 'OIDFJIODSFJIODSFJIU(WFHOISDF903248uweriy87345ureiyrtb965258752475201258525475sduri6838ejmfiuvmknmeujdjedjdjjdjdjdjd)'
        payload = {
        'random_number': random_number,
        'uuid': my_uuid,
        'hashed_data': hashed_data,
        'Server Key': 'OIDFJIODSFJIODSFJIU(WFHOISDF903248uweriy87345ureiyrtb965258752475201258525475sduri6838ejmfiuvmknmeujdjedjdjjdjdjdjd)',
        'RSA': list(RSA.generate(2048)),
        'exp': expiration_time,
    }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        context = {'token': token}
        return JsonResponse(context, status=200)

