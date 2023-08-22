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

class Instruction(models.Model):
    Header = models.TextField(blank=True)
    Date = models.DateField(blank=True)
    Paragraph = models.TextField(blank=True)
    Paragraph2 = models.TextField(blank=True)
    Paragraph3 = models.TextField(blank=True)
    Paragraph4 = models.TextField(blank=True)
    Paragraph5 = models.TextField(blank=True)
    Paragraph6 = models.TextField(blank=True)
    Paragraph7 = models.TextField(blank=True)
    Paragraph8 = models.TextField(blank=True)
    Paragraph9 = models.TextField(blank=True)
    Paragraph10 = models.TextField(blank=True)
    Paragraph11 = models.TextField(blank=True)

class Text(models.Model):
    One = models.TextField(blank=True)
    Two = models.TextField(blank=True)
    Date = models.DateTimeField(blank=True)

# Create your models here.
#j
