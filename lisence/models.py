
from django.db import models

# Create your models here.
class lisence(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=255, primary_key=True)
    Type = models.CharField(max_length=100)
    Activations = models.IntegerField()
    Limit = models.IntegerField()
    