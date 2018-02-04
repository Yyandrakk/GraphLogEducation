from django import forms
from .models import CursoMoodle

class FormCursoMoodle(forms.ModelForm):

    class Meta():
        model = CursoMoodle
        fields = ("nombre","desc","umbral", "documento")

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("instance", None)
        super(FormCursoMoodle,self).__init__(*args,**kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'

        self.fields['documento'].widget.attrs['class'] = 'form-control-file'

    def clean(self):
        datos = super(FormCursoMoodle,self).clean()

        nombre = datos['nombre']

        if CursoMoodle.objects.filter(nombre=nombre,profesor_id=self.user.id).exists():
            raise forms.ValidationError({
                'nombre': forms.ValidationError('Ya tiene un curso con ese nombre', code='invalid'),
            })

        return datos




