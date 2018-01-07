from django import forms

from .models import Usuario


class FormLogin(forms.ModelForm):
    class Meta():
        model = Usuario
        fields = ['username','password']

    def __init__(self,*args,**kargs):
        super(FormLogin,self).__init__(*args,**kargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'



class FormRegister(forms.ModelForm):

    val_password = forms.CharField(widget=forms.PasswordInput(),label='Confirma la contraseña')

    class Meta():
        model = Usuario
        fields = ('username','email','password','first_name','last_name')

    def __init__(self,*args,**kargs):
        super(FormRegister,self).__init__(*args,**kargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        datos = super(FormRegister,self).clean()
        passw1 = datos.get("password")
        passw2 = datos.get("val_password")

        if passw1 != passw2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return datos

