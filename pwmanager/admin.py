from django.contrib import admin
from .models import Password, Secret, Encryption
# Register your models here.
admin.site.register(Password)
admin.site.register(Secret)
admin.site.register(Encryption)

