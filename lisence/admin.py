from django.contrib import admin
from .models import lisence, RegDevice, LinkedUser, AcessRequest, ConfCode
admin.site.register(lisence)
admin.site.register(RegDevice)
admin.site.register(LinkedUser)
admin.site.register(AcessRequest)
admin.site.register(ConfCode)

# Register your models here.
