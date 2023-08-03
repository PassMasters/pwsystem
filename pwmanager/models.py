from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_size
from datetime import date
from django.contrib.auth.models import User
from django.utils.timezone import *
from cryptography.fernet import Fernet
import os
import base64
import django

    

# Create your models here.
class PW(models.Model):
    Username = models.CharField(max_length=255, blank=True)
    Password = models.CharField(max_length=255, blank=True)
    URL = models.URLField(blank=True, default="google.com")
    TOTP = models.CharField(max_length=255, blank=True)
    Atachment = models.FileField(validators=[validate_file_size], default='jkasdflajsdf')
    Date_Created = models.DateField(default='django.utils.timezone.now')
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Owner_ID = models.IntegerField( blank=True, default='0000', editable=False)
    Notes = models.CharField(blank=True, max_length=500, default="this is blank")
    id = models.BigAutoField(primary_key=True) #from da chat gpt
    
class Encryption(models.Model):
   Owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   Owner_ID = models.IntegerField(blank=True, editable=False, default=824523555)
   Salt = models.CharField(max_length=500, default="0")


        


class Secret(models.Model):
    Name = models.CharField(max_length=255, blank=True)
    Website = models.CharField(max_length=255, blank=True)
    Id = models.IntegerField( blank=True, default='0000',  primary_key=True, editable=False)
    Secret_key = models.CharField(max_length=255, blank=True)
