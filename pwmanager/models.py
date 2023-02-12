from django.db import models

from .validators import validate_file_size
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
import base64



# Create your models here.
class Password(models.Model):
    Username = models.CharField(max_length=255, blank=True)
    Password = models.CharField(max_length=255, blank=True)
    TOTP = models.CharField(max_length=255, blank=True)
    Atachment = models.FileField(validators=[validate_file_size], default='jkasdflajsdf')
    Date_Created = models.DateField(default='2023-02-01')
    Owner = models.CharField(max_length=255, blank=True)
    Id = models.IntegerField( blank=True, default='0000')
    
    
class Encryption(models.Model):
   Owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   Id = models.IntegerField( blank=True, default='0000')
   Salt = models.CharField(max_length=255, default="0")


        


class Secret(models.Model):
    Name = models.CharField(max_length=255, blank=True)
    Website = models.CharField(max_length=255, blank=True)
    Key_ID = models.CharField(max_length=255, blank=True)
    Secret_key = models.CharField(max_length=255, blank=True)
