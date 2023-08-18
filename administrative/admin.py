from django.contrib import admin
from .models import Issue, Link

class IssueAdmin(admin.ModelAdmin):
    list_display = ('Issue', 'Date')

class LinkAdmin(admin.ModelAdmin):
    list_display = ('Title', 'HyperLink')    

admin.site.register(Issue, IssueAdmin)
admin.site.register(Link, LinkAdmin)


# Register your models here.
#j
