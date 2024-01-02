
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class lisence(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=255, primary_key=True)
    Type = models.CharField(max_length=100)
    Activations = models.IntegerField()
    Limit = models.IntegerField()
    

class client(models.Model):
    Name = models.CharField(max_length=100)
    Serial = models.BigIntegerField(primary_key=True)
    key = models.ManyToManyField(lisence, on_delete=models.CASCADE)
    Signkey = models.CharField(max_length=500)

class PWacess(models.Model):
    User = models.ManyToManyField(User)
    Client = models.ManyToManyField(client)
    Token = models.CharField(max_length=1024)
    

class DevAcessKey(models.Model):
    Key = models.CharField(max_length=1024)
    Org = models.CharField(max_length=100)