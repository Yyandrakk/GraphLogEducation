from django import forms

from .models import CursoMoodle


class FormCursoMoodle(forms.ModelForm):

    class Meta():
        model = CursoMoodle
        fields = ("nombre","desc","umbral", "documento")
        help_texts = {
            'nombre': ('Titulo del curso'),
        }
        error_messages = {
            'nombre': {
                'max_length': ("Ha superado el tamaño maximo"),
            },
        }

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("instance", None)
        super(FormCursoMoodle,self).__init__(*args,**kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'

        self.fields['documento'].widget.attrs['class'] = 'custom-file-input'

    def clean(self):
        datos = super(FormCursoMoodle,self).clean()

        nombre = datos['nombre']

        if CursoMoodle.objects.filter(nombre=nombre,profesor_id=self.user.id).exists():
            raise forms.ValidationError({
                'nombre': forms.ValidationError('Ya tiene un curso con ese nombre', code='invalid'),
            })

        return datos

class FormUpdateCMoodle(forms.ModelForm):

    class Meta():
        model = CursoMoodle
        fields = ["desc","umbral", "documento"]


    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop("instance", None)
        super(FormUpdateCMoodle,self).__init__(*args,**kwargs)
        for v in self.visible_fields():
            v.field.required = False
            v.field.widget.attrs['class'] = 'form-control'

        self.fields['documento'].widget.attrs['class'] = 'custom-file-input'
        self.fields['documento'].required = False

    def clean(self):
        datos = super(FormUpdateCMoodle,self).clean()
        return datos

    def save(self, commit=True):
        instance = super(FormUpdateCMoodle, self).save(commit=False)

        if commit:
            instance.save(update_fields=self.changed_data)

        return instance







