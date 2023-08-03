from django.contrib import admin
from .models import Password, Secret, Encryption, PwUser
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User




# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = PwUser
    can_delete = False
    verbose_name_plural = "PwUsers"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]


# Re-register UserAdmin
admin.site.unregister(PwUser)
admin.site.register(PwUser, UserAdmin)
admin.site.register(Password)
admin.site.register(Secret)
admin.site.register(Encryption)

