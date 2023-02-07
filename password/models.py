from django.db import models
from .validators import validate_file_size
# Create your models here.
class Password(models.Model):
    Username = models.CharField(max_length=255, blank=True)
    Password = models.CharField(max_length=255, blank=True)
    TOTP = models.CharField(max_length=255, blank=True)
    Atachment = models.FileField(validators=[validate_file_size])
    Date_Created = models.DateField()