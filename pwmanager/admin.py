from django.contrib import admin
from .models import PW, Secret, Encryption
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User




# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton



# Define a new User admin



admin.site.register(PW)
admin.site.register(Secret)
admin.site.register(Encryption)

