import json
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
# Ensure users go through the allauth workflow when logging into admin.
def Version(request):
    DownloadURL = "https://azureblob"
    Version = "1.0.0 Beta"
    result ={
        'URl': DownloadURL,
        'Version': Version,
        }
    return JsonResponse(result, status=200)