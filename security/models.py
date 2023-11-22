from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Device(models.Model):
    Name = models.CharField(max_length=255)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Pub_key = models.CharField(max_length=1024)
    UID = models.CharField(max_length=255, primary_key=True)


class keytransfer(models.Model):
    Name = models.ForeignKey(User, on_delete=models.CASCADE)
    Device = models.ForeignKey(Device, on_delete=models.CASCADE)
    UID = models.CharField(max_length=255, primary_key=True)
class UserServerKeys(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=1024, default="1")

