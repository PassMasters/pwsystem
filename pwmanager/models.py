
from django.db import models
from django.urls import reverse
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
    Atachment = models.FileField(validators=[validate_file_size], default='jkasdflajsdf', blank=True)
    Date_Created = models.DateField(default=django.utils.timezone.now)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Notes = models.CharField(blank=True, max_length=500, default="this is blank") 

    def get_absolute_url(self):
        return reverse('edit', args=[self.id])

    
class Encryption(models.Model):
   Owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   Owner_ID = models.BigIntegerField(blank=True,  default=82452355)
   Salt = models.CharField(max_length=500, default="0")
   IV = models.CharField(max_length=500, default="0")

class Data_ID(models.Model):
    Key_lookup = models.BigIntegerField(blank=True,  default=82452555)
    User = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        


class Secret(models.Model):
    Name = models.CharField(max_length=255, blank=True)
    Website = models.CharField(max_length=255, blank=True)
    Id = models.IntegerField( blank=True, default='0000',  primary_key=True, editable=False)
    Secret_key = models.CharField(max_length=255, blank=True)

class PWcheck(models.model):
   Owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   Owner_ID = models.BigIntegerField(blank=True,  default=82452355)
   Test_PW = models.CharField(max_length=500, blank=True)
   Answer = models.CharField(max_length=500, blank=True)