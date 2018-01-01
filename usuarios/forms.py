from django import forms

from .models import Usuario


class FormLogin(forms.ModelForm):
    class Meta:
        model =  Usuario
        fields = ['username','password']


class FormRegister(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = '__all__'