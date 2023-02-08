from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from .validators import validate_file_size
from django.contrib.auth.models import User

# Create your models here.
class Password(models.Model):
    Username = models.CharField(max_length=255, blank=True)
    Password = EncryptedCharField(max_length=255, blank=True)
    TOTP = models.CharField(max_length=255, blank=True)
    Atachment = models.FileField(validators=[validate_file_size], default='jkasdflajsdf')
    Date_Created = models.DateField(default='2023-02-01')
    
   


        


class Secret(models.Model):
    Name = models.CharField(max_length=255, blank=True)
    Website = models.CharField(max_length=255, blank=True)
    Key_ID = models.CharField(max_length=255, blank=True)
    Secret_key = models.CharField(max_length=255, blank=True)
