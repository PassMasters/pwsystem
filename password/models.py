from django.db import models

# Create your models here.
class Password(models.Model):
    Username = models.CharField(max_length=255, blank=True)
    Password = models.CharField(max_length=255, blank=True)
    TOTP = models.CharField(max_length=255, blank=True)
