from pyexpat import model
from .models import PW, Encryption, Data_ID
from django import forms

class PwEdit(forms.ModelForm):
    class Meta:
        model = PW
        fields = '__all__'
