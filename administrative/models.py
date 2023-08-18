from django.db import models

class Issue(models.Model):
   Issue = models.CharField(max_length=280)
   Date = models.DateField(blank=True)
   One_Detail = models.CharField(max_length=280, blank=True)
   Second_Detail = models.CharField(max_length=280, blank=True)
   Third_Detail = models.CharField(max_length=280, blank=True)


class Link(models.Model):
    Title = models.CharField(max_length=280)
    HyperLink = models.CharField(max_length=280)


# Create your models here.
#j
