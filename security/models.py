from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Device(models.Model):
    Name = models.CharField(max_length=255)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Pub_key = models.CharField(max_length=1024, default="10000", primary_key=True)

class UserServerKeys(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=1024, default="1")

