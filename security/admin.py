from django.contrib import admin
from .models import Device, UserServerKeys, Devsesion
# Register your models here.
admin.site.register(Device)
admin.site.register(UserServerKeys)
admin.site.register(Devsesion)
