import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CursoMoodle, EstudianteCursoMoodle, MaterialCursoMoodle, TiempoDedicadoCursoMoodle


@receiver(post_save, sender=CursoMoodle)
def creacion_informacion_curso(sender,instance,created, **kwargs):

    if created:
        df = pd.read_csv(instance.documento)
        n_unicos = filter(lambda n: n != '-' and "Administrador" not in n, df['Nombre completo del usuario'].unique())

        for name in n_unicos:
            alumno = EstudianteCursoMoodle(nombre=name,curso=instance)
            alumno.save()

        func = lambda s: s.split(':')[1].strip()
        fil_arc = df[df['Contexto del evento'].str.contains("Archivo:")]
        fil_cues = df[df['Contexto del evento'].str.contains("Cuestionario:")]
        arc_unicos = set(map(func,fil_arc['Contexto del evento'].unique()))
        cues_unicos = set(map(func, fil_cues['Contexto del evento'].unique()))

        for name in arc_unicos:
            archivo = MaterialCursoMoodle(nombre=name,curso=instance,tipo=MaterialCursoMoodle.ARCHIVO)
            archivo.save()

        for name in cues_unicos:
             cuestionario = MaterialCursoMoodle(nombre=name, curso=instance, tipo=MaterialCursoMoodle.CUESTIONARIO)
             cuestionario.save()

        for fila in pd.DataFrame({'count': df.groupby(pd.Grouper(key='Hora', freq='D')).size()}).reset_index().iterrows():
            dia=TiempoDedicadoCursoMoodle(curso=instance,timestamp=pd.to_datetime(fila['Hora'], unit='s'),contador=fila["count"],tipo=TiempoDedicadoCursoMoodle.DIA)
            dia.save()

        CursoMoodle.objects.filter(pk=instance.pk).update(procesado=True)



    else:
        if "documento" is kwargs.get("update_fields",False):
            print("documento")

