import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CursoMoodle, EstudianteCursoMoodle, MaterialCursoMoodle, TiempoDedicadoCursoMoodle, \
    TiempoDedicadoEstudianteCursoMoodle


@receiver(post_save, sender=CursoMoodle)
def creacion_informacion_curso(sender,instance,created, **kwargs):

    if created:

        dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M')
        df = pd.read_csv(instance.documento,parse_dates=['Hora'], date_parser=dateparse, dayfirst=True)
        filter = df.apply(lambda fila: fila.iloc[1] != '-' and "Administrador" not in fila.iloc[1], axis=1)
        df = df[filter]
        n_unicos = df['Nombre completo del usuario'].unique()

        for name in n_unicos:
            alumno = EstudianteCursoMoodle(nombre=name.strip(),curso=instance)
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

        auxDiasDf = pd.DataFrame({'count': df.groupby(pd.Grouper(key='Hora', freq='D')).size()}).reset_index()
        for fila in auxDiasDf.itertuples():
            dia=TiempoDedicadoCursoMoodle(curso=instance,timestamp=pd.to_datetime(fila.Hora, unit='s'),contador=fila.count,tipo=TiempoDedicadoCursoMoodle.DIA)
            dia.save()

        times = pd.DatetimeIndex(df['Hora'])
        for fila in pd.DataFrame({'count':df.groupby([times.hour]).size()}).reset_index().itertuples():
            hora = TiempoDedicadoCursoMoodle(curso=instance, timestamp=pd.to_datetime(fila.Hora, unit='h'),
                                            contador=fila.count, tipo=TiempoDedicadoCursoMoodle.HORA)
            hora.save()

        std_name=''
        aux_std = None
        for fila in pd.DataFrame({'count': df.groupby([pd.Grouper(key='Nombre completo del usuario'),pd.Grouper(key='Hora', freq='D')]).size()}).reset_index().itertuples():
            if std_name != fila._1.strip():
                aux_std = EstudianteCursoMoodle.objects.filter(nombre=fila._1.strip(),curso=instance).first()
                std_name = aux_std.nombre

            dia = TiempoDedicadoEstudianteCursoMoodle(curso=instance, timestamp=pd.to_datetime(fila.Hora, unit='s'),
                                            contador=fila.count, tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD, estudiante=aux_std)
            dia.save()

        std_name = ''
        aux_std = None
        for fila in pd.DataFrame({'count': df.groupby([pd.Grouper(key='Nombre completo del usuario'), times.hour]).size()}).reset_index().itertuples():
            if std_name != fila._1.strip():
                aux_std = EstudianteCursoMoodle.objects.filter(nombre=fila._1.strip(), curso=instance).first()
                std_name = aux_std.nombre

            dia = TiempoDedicadoEstudianteCursoMoodle(curso=instance, timestamp=pd.to_datetime(fila.Hora, unit='h'),
                                                      contador=fila.count,
                                                      tipo=TiempoDedicadoEstudianteCursoMoodle.HORA_STD,
                                                      estudiante=aux_std)
            dia.save()

        CursoMoodle.objects.filter(id=instance.id).update(procesado=True)
        instance.refresh_from_db()
        

    else:
        if "documento" is kwargs.get("update_fields",False):
            print("documento")

