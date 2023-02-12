from django.db import models

class Issue(models.Model):
   Issue = models.CharField(max_length=280)
   One_Detail = models.CharField(max_length=280)

class Link(models.Model):
    Title = models.CharField(max_length=280)
    HyperLink = models.CharField(max_length=280)


# Create your models here.
#j
