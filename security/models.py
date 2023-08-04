from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Device(models.Model):
    Name = models.CharField(max_length=255)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Device_UUID = models.CharField(max_length=1024)
    Cookie_ID = models.CharField(max_length=1024)
    Salt = models.CharField(max_length=500)