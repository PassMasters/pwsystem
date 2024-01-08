
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AcessRequest(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    key  = models.CharField(max_length=255)
    premisions = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class ConfCode(models.Model):
    req = models.OneToOneField(AcessRequest, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, primary_key=True)
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
    premisions = models.CharField(max_length=1024, default="NONE")
    