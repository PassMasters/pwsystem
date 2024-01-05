
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class lisence(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=255, primary_key=True)
    Type = models.CharField(max_length=100)
    Activations = models.IntegerField()
    Limit = models.IntegerField()

class RegDevice(models.Model):
    key = models.CharField(max_length=255)
    Serial = models.CharField(max_length=255, primary_key=True)
    
class LinkedUser(models.Model):
    Device = models.ForeignKey(RegDevice, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Key = models.CharField(max_length=255)
    