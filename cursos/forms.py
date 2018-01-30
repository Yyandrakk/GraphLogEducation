from django import forms
from .models import CursoMoodle

class FormCursoMoodle(forms.ModelForm):

    class Meta():
        model = CursoMoodle
        fields = ("nombre","desc","umbral")


    def __init__(self,*args,**kargs):
        super(FormCursoMoodle,self).__init__(*args,**kargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'



