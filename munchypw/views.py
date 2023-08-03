from django.contrib import admin

from django.contrib.admin.views.decorators import staff_member_required

# Ensure users go through the allauth workflow when logging into admin.
admin.site.login = staff_member_required(admin.site.login, login_url='/accounts/login')
# Run the standard admin set-up.
admin.autodiscover()
