
from django import forms
from django.forms import ModelForm

from .models import Password

class PasswordForm(ModelForm):
    Username = forms.TextInput()
    Password = forms.TextInput()
    TOTP = forms.TextInput()
    Atachment = forms.FileField()
    class Meta:
        model = Password
        fields = ['Username', 'Password', 'TOTP', 'Atachment']