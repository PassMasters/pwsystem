from django.contrib import admin
from .models import Issue, Link, Instruction

class IssueAdmin(admin.ModelAdmin):
    list_display = ('Issue', 'Date')

class LinkAdmin(admin.ModelAdmin):
    list_display = ('Title', 'HyperLink') 

class InstructionAdmin(admin.ModelAdmin):
    list_display = ('Header','Date')

admin.site.register(Issue, IssueAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Instruction, InstructionAdmin)
