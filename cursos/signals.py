import threading

import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CursoMoodle, EstudianteCursoMoodle, MaterialCursoMoodle, TiempoDedicadoCursoMoodle, \
    TiempoDedicadoEstudianteCursoMoodle, TiempoInvertidoMaterialCursoMoodle, TiempoInvertidoEstudianteCursoMoodle


class ProcesarFicheroThread(threading.Thread):
    def __init__(self, curso,solo_umbral ,**kwargs):
        self.instance = curso
        self.todo = not solo_umbral
        super(ProcesarFicheroThread, self).__init__(**kwargs)

    def run(self):
        dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M')
        df = pd.read_csv(self.instance.documento, parse_dates=['Hora'], date_parser=dateparse, dayfirst=True)
        filter = df.apply(lambda fila: fila.iloc[1] != '-' and "Administrador" not in fila.iloc[1], axis=1)
        df = df[filter]

        if self.todo:
            n_unicos = df['Nombre completo del usuario'].unique()

            for name in n_unicos:
                alumno = EstudianteCursoMoodle(nombre=name.strip(), curso=self.instance)
                alumno.save()

            func = lambda s: s.split(':')[1].strip()
            fil_arc = df[df['Contexto del evento'].str.contains("Archivo:")]
            fil_cues = df[df['Contexto del evento'].str.contains("Cuestionario:")]
            arc_unicos = set(map(func, fil_arc['Contexto del evento'].unique()))
            cues_unicos = set(map(func, fil_cues['Contexto del evento'].unique()))

            for name in arc_unicos:
                archivo = MaterialCursoMoodle(nombre=name.strip(), curso=self.instance, tipo=MaterialCursoMoodle.ARCHIVO)
                archivo.save()

            for name in cues_unicos:
                cuestionario = MaterialCursoMoodle(nombre=name.strip(), curso=self.instance, tipo=MaterialCursoMoodle.CUESTIONARIO)
                cuestionario.save()

            for fila in pd.DataFrame({'count': fil_arc.groupby(pd.Grouper(key='Contexto del evento')).size()}).reset_index().itertuples():
                archivo = MaterialCursoMoodle.objects.filter(nombre=fila._1.split(':')[1].strip(), curso=self.instance,
                                              tipo=MaterialCursoMoodle.ARCHIVO).first()
                archivo.contador = fila.count
                archivo.save()

            auxDiasDf = pd.DataFrame({'count': df.groupby(pd.Grouper(key='Hora', freq='D')).size()}).reset_index()
            for fila in auxDiasDf.itertuples():
                dia = TiempoDedicadoCursoMoodle(curso=self.instance, timestamp=pd.to_datetime(fila.Hora, unit='s'),
                                                contador=fila.count, tipo=TiempoDedicadoCursoMoodle.DIA)
                dia.save()

            times = pd.DatetimeIndex(df['Hora'])
            for fila in pd.DataFrame({'count': df.groupby([times.hour]).size()}).reset_index().itertuples():
                hora = TiempoDedicadoCursoMoodle(curso=self.instance, timestamp=pd.to_datetime(fila.Hora, unit='h'),
                                                 contador=fila.count, tipo=TiempoDedicadoCursoMoodle.HORA)
                hora.save()

            std_name = ''
            aux_std = None
            for fila in pd.DataFrame({'count': df.groupby([pd.Grouper(key='Nombre completo del usuario'),
                                                           pd.Grouper(key='Hora',
                                                                      freq='D')]).size()}).reset_index().itertuples():
                if std_name != fila._1.strip():
                    aux_std = EstudianteCursoMoodle.objects.filter(nombre=fila._1.strip(), curso=self.instance).first()
                    std_name = aux_std.nombre

                dia = TiempoDedicadoEstudianteCursoMoodle(curso=self.instance, timestamp=pd.to_datetime(fila.Hora, unit='s'),
                                                          contador=fila.count,
                                                          tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD,
                                                          estudiante=aux_std)
                dia.save()

            std_name = ''
            aux_std = None
            times = pd.DatetimeIndex(df['Hora'])
            for fila in pd.DataFrame({'count': df.groupby(
                    [pd.Grouper(key='Nombre completo del usuario'), times.hour]).size()}).reset_index().itertuples():
                if std_name != fila._1.strip():
                    aux_std = EstudianteCursoMoodle.objects.filter(nombre=fila._1.strip(), curso=self.instance).first()
                    std_name = aux_std.nombre

                dia = TiempoDedicadoEstudianteCursoMoodle(curso=self.instance, timestamp=pd.to_datetime(fila.Hora, unit='h'),
                                                          contador=fila.count,
                                                          tipo=TiempoDedicadoEstudianteCursoMoodle.HORA_STD,
                                                          estudiante=aux_std)

                dia.save()


            std_name = ''
            fecha_anterior = None
            aux_contexto = None
            for fila in df.loc[df['Nombre evento'].isin(['Ha comenzado el intento', 'Intento enviado'])].sort_values(
                    by=['Nombre completo del usuario', 'Contexto del evento', 'Hora']).itertuples():
                if std_name != fila._2.strip():
                    aux_std = EstudianteCursoMoodle.objects.filter(nombre=fila._2.strip(), curso=self.instance).first()
                    std_name = aux_std.nombre
                    aux_contexto = None
                fecha = pd.to_datetime(fila.Hora, unit='s')
                if fila._6 == 'Ha comenzado el intento':
                    try:
                        aux_contexto = MaterialCursoMoodle.objects.filter(nombre=fila._4.split(':')[1].strip(),
                                                                          curso=self.instance,
                                                                          tipo=MaterialCursoMoodle.CUESTIONARIO).first()
                        fecha_anterior = fecha
                    except IndexError:
                        aux_contexto = None
                elif aux_contexto != None and (fecha - fecha_anterior).seconds > 0:
                    t = TiempoInvertidoMaterialCursoMoodle(curso=self.instance, estudiante=aux_std,
                                                     seconds=(fecha - fecha_anterior).seconds,
                                                     contexto=aux_contexto)
                    t.save()

        std_name = ''
        aux_std = None
        time_invertido = 0
        fecha_anterior = None
        umbral_sec = self.instance.umbral * 60
        for fila in df.sort_values(by=['Nombre completo del usuario', 'Hora']).itertuples():
            if std_name != fila._2.strip():
                if std_name != '':
                    t = TiempoInvertidoEstudianteCursoMoodle(curso=self.instance, estudiante=aux_std,timestamp=pd.to_datetime(fecha_anterior._date_repr,format='%Y-%m-%d') ,seconds=time_invertido)
                    t.save()
                aux_std = EstudianteCursoMoodle.objects.filter(nombre=fila._2.strip(), curso=self.instance).first()
                std_name = aux_std.nombre
                time_invertido = 0
            fecha = pd.to_datetime(fila.Hora, unit='s')
            if fecha_anterior != None and (fecha - fecha_anterior).seconds < umbral_sec:
                time_invertido += (fecha - fecha_anterior).seconds
            elif fecha_anterior != None and fecha_anterior.strftime("%y-%m-%d") != fecha.strftime("%y-%m-%d"):
                t = TiempoInvertidoEstudianteCursoMoodle(curso=self.instance, estudiante=aux_std,
                                                         timestamp=pd.to_datetime(fecha_anterior._date_repr, format='%Y-%m-%d'),
                                                         seconds=time_invertido)
                t.save()
                time_invertido = 0

            fecha_anterior = fecha

        CursoMoodle.objects.filter(id=self.instance.id).update(procesado=True)
        self.instance.refresh_from_db()



@receiver(post_save, sender=CursoMoodle)
def creacion_informacion_curso(sender,instance,created, **kwargs):

    if created:
        ProcesarFicheroThread(instance,False).start()
    else:
        update_fields = kwargs.get("update_fields")
        if update_fields!=None and "documento" in update_fields:
            CursoMoodle.objects.filter(id=instance.id).update(procesado=False)
            instance.refresh_from_db()
            EstudianteCursoMoodle.objects.filter(curso=instance).delete()
            MaterialCursoMoodle.objects.filter(curso=instance).delete()
            TiempoDedicadoCursoMoodle.objects.filter(curso=instance).delete()
            TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso=instance).delete()
            TiempoInvertidoMaterialCursoMoodle.objects.filter(curso=instance).delete()
            TiempoInvertidoEstudianteCursoMoodle.objects.filter(curso=instance).delete()
            ProcesarFicheroThread(instance, False).start()
        elif  update_fields!=None and "umbral" in update_fields:
            CursoMoodle.objects.filter(id=instance.id).update(procesado=False)
            instance.refresh_from_db()
            TiempoInvertidoEstudianteCursoMoodle.objects.filter(curso=instance).delete()
            ProcesarFicheroThread(instance, True).start()


