from django import forms

from .models import Usuario


class FormLogin(forms.ModelForm):
    class Meta():
        model = Usuario
        fields = ['username','password']


class FormRegister(forms.ModelForm):

    val_password = forms.CharField(widget=forms.PasswordInput(),label='Confirma la contraseña')

    class Meta():
        model = Usuario
        fields = ('username','email','password','first_name','last_name')