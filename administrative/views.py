from django.shortcuts import render
from .models import Link, Issue

def dev_home(request):
        issues = Issue.objects.all()
        links = Link.objects.all()
        return render(request, "version.html",  {'issues':issues,'links':links})


# Create your views here.
