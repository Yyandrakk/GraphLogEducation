import json
from datetime import datetime

from django.db.models import Sum, Avg
from django.db.models.functions import ExtractWeek, ExtractYear

from cursos.models import TiempoDedicadoCursoMoodle, TiempoDedicadoEstudianteCursoMoodle, \
    TiempoInvertidoMaterialCursoMoodle, \
    CursoMoodle, TiempoInvertidoEstudianteCursoMoodle, MaterialCursoMoodle

colors = ['#8bc34a','#00cc66']

def graficaTiempo(id_curso, id_std=None, idsGN=None):
    chart = {'type': 'line'}
    dataset = []
    if idsGN!=None:
        i = 0
        for idGN in json.loads(idsGN):
            dias = TiempoDedicadoCursoMoodle.objects.filter(curso_id=idGN, tipo=TiempoDedicadoCursoMoodle.DIA)
            count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=idGN,
                                                             tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(
                total=Sum('contador'))
            data = []
            for dia in dias:
                data.append({'x': format(dia.timestamp, "%d/%m/%Y"), 'y': ((dia.contador / count['total']) * 100)})
            curso = CursoMoodle.objects.filter(id=idGN).first()
            dataset.append({'data': data, 'borderColor': colors[i], 'label': '%Eventos '+curso.nombre})
            i+=1

    elif id_std!=None:
        dias = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD)
        count = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD).aggregate(
            total=Sum('contador'))
        data = []
        for dia in dias:
            data.append({'x':format(dia.timestamp, "%d/%m/%Y"),'y':((dia.contador / count['total']) * 100)})
        dataset.append({'data': data, 'borderColor': "#3e65cd", 'label': '%Eventos estudiante'})

    dias = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA)
    count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(
            total=Sum('contador'))
    data = []
    for dia in dias:
       data.append({'x':format(dia.timestamp, "%d/%m/%Y"),'y':((dia.contador / count['total']) * 100)})

    dataset.append({'data': data, 'borderColor': "#3e95cd", 'label': '%Eventos general'})
    chart['data'] = {'datasets': dataset}
    chart['options'] = {'scales': {'xAxes':[{'type':'time','time':{'unit':'day','round':'day','parser':'D/M/YYY'} }]},
                        'title': {
                            'display': 'true',
                            'text': 'Eventos en cada dia',
                            'fontSize': 16
                        }
                        }

    return chart


def graficaTiempoSemanal(id_curso, id_std=None,idsGN=None):
    chart = {'type': 'line'}
    dataset = []
    data = []
    if idsGN!=None:
        i = 0
        for idGN in json.loads(idsGN):
            count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso,
                                                             tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(
                total=Sum('contador'))
            semanas = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso,
                                                               tipo=TiempoDedicadoCursoMoodle.DIA).annotate(
                week=ExtractWeek('timestamp')).values('week').annotate(s=Sum('contador')).values('week', 's').annotate(
                anyo=ExtractYear('timestamp')).values('week', 'anyo', 's').order_by('week')
            data = []
            for semana in semanas:
                data.append({'x': datetime.strptime(str(semana['anyo']) + ' ' + str(semana['week']) + ' 1',
                                                    "%Y %W %w").strftime("%d/%m/%Y"),
                             'y': ((semana['s'] / count['total']) * 100)})
            curso = CursoMoodle.objects.filter(id=idGN).first()
            dataset.append({'data': data, 'borderColor': colors[i], 'label': '%Eventos '+curso.nombre})
            i+=1
    elif id_std != None:
        semanas = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD).annotate(
            week=ExtractWeek('timestamp')).values('week').annotate(s=Sum('contador')).values('week', 's').annotate(anyo=ExtractYear('timestamp')).values('week','anyo', 's').order_by('week')
        count = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std,
                                                         tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD).aggregate(total=Sum('contador'))
        for semana in semanas:
            data.append({'x': datetime.strptime(str(semana['anyo']) + ' ' + str(semana['week']) + ' 1',"%Y %W %w").strftime("%d/%m/%Y"),'y': ((semana['s'] / count['total']) * 100)})
        dataset.append({'data': data, 'borderColor': "#3e65cd", 'label': '%Eventos estudiante'})


    count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(
        total=Sum('contador'))
    semanas = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).annotate(
        week=ExtractWeek('timestamp')).values('week').annotate(s=Sum('contador')).values('week', 's').annotate(anyo=ExtractYear('timestamp')).values('week','anyo', 's').order_by('week')
    data = []
    for semana in semanas:
        data.append({'x':datetime.strptime(str(semana['anyo']) +' ' + str(semana['week']) + ' 1', "%Y %W %w").strftime("%d/%m/%Y"),'y':((semana['s'] / count['total']) * 100)})

    dataset.append({'data': data, 'borderColor': "#3e95cd", 'label': '%Eventos general'})
    chart['data'] = {'datasets': dataset}

    chart['options'] = {'scales': {'xAxes': [{'type': 'time', 'time': {'unit': 'day', 'round': 'day', 'parser': 'D/M/YYY'}}]},
                        'title': {
                            'display': 'true',
                            'text': 'Eventos en cada semana',
                            'fontSize':16
                        }
                        }

    return chart


def graficaTiempoHora(id_curso, id_std=None):

    chart = {'type': 'bar'}
    labels = []
    data = []
    dataset = []

    if id_std != None:
        horas = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.HORA_STD)
        count = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.HORA_STD).aggregate(
            total=Sum('contador'))
        for hora in horas:
            data.append((hora.contador / count['total']) * 100)

        dataset.append({'data': data, 'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9",
                                                          "#c45850", "#C4A73D", "#7EC44A", "#C44148",
                                                          "#C4249F", "#110EC4", "#AF19FF", "#18FFDD",
                                                          "#FFD558", "#3e96cd", "#5e5ea2", "#3c3a9f",
                                                          "#e823b9", "#c45810", "#CAA73D", "#7E444A",
                                                          "#C43148", "#C4219F", "#113EC4", "#AF29FF",
                                                          "#18FFAD"], 'label': '%Eventos estudiante'})

    horas = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.HORA)
    count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.HORA).aggregate(
        total=Sum('contador'))

    data = []
    for hora in horas:
        labels.append(format(hora.timestamp, "%H"))
        data.append((hora.contador / count['total']) * 100)

    dataset.append({'data': data,'backgroundColor': ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9",
                                                     "#c45850", "#C4A73D", "#7EC44A", "#C44148",
                                                     "#C4249F", "#110EC4", "#AF19FF", "#18FFDD",
                                                     "#FFD558", "#3e96cd", "#5e5ea2", "#3c3a9f",
                                                     "#e823b9", "#c45810", "#CAA73D", "#7E444A",
                                                     "#C43148", "#C4219F", "#113EC4", "#AF29FF",
                                                     "#18FFAD"], 'label': '%Eventos'})

    chart['data'] = {'labels': labels, 'datasets': dataset}
    chart['options'] = {'title': {
                            'display': 'true',
                            'text': 'Eventos en cada hora',
                            'fontSize': 16
                            }
                        }
    return chart


def graficaTiempoMedioContexto(id_curso,id_std=None):

    chart = {'type': 'bar'}
    labels = []
    data = []
    dataset = []

    if id_std!=None:
        for cuestionario in TiempoInvertidoMaterialCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std).exclude(
                contexto__isnull=True).values('contexto__nombre').annotate(media=Avg('seconds')).order_by( 'contexto__nombre'):
            labels.append(cuestionario['contexto__nombre'])
            data.append(cuestionario['media'] / 60)
        texto = 'Tiempo en cada cuestionario'
    else:
        for cuestionario in TiempoInvertidoMaterialCursoMoodle.objects.filter(curso_id=id_curso).exclude(contexto__isnull=True).values('contexto__nombre').annotate(media=Avg('seconds')).order_by('contexto__nombre'):
            labels.append(cuestionario['contexto__nombre'])
            data.append(cuestionario['media']/60)
        texto = 'Tiempo medio en cada cuestionario'

    dataset.append({'data': data, 'label': 'Minutos','backgroundColor':"#3e95cd"})

    chart['data'] = {'labels': labels, 'datasets': dataset}
    chart['options'] = {'scales': {'xAxes': [{'ticks': {'minRotation': 85}}]},
                        'title': {
                            'display': 'true',
                            'text': texto,
                            'fontSize': 16
                        }
                        }
    return chart

def graficaUsoArchivos(id_curso):

    chart = {'type': 'bar'}
    labels = []
    data = []
    dataset = []
    count = MaterialCursoMoodle.objects.filter(curso_id=id_curso,
                                               tipo=MaterialCursoMoodle.ARCHIVO).aggregate(
        total=Sum('contador'))

    for archivo in MaterialCursoMoodle.objects.filter(curso_id=id_curso,
                                              tipo=MaterialCursoMoodle.ARCHIVO).order_by('nombre'):
        labels.append(archivo.nombre)
        data.append((archivo.contador/ count['total'])*100)

    dataset.append({'data': data, 'label': '%Eventos','backgroundColor':"#3e95cd"})

    chart['data'] = {'labels': labels, 'datasets': dataset}
    chart['options'] = {'scales': {'xAxes': [{'ticks': {'minRotation': 85}}]},
                        'title': {
                            'display': 'true',
                            'text': 'Uso de archivos',
                            'fontSize': 16
                        }
                        }
    return chart

def graficaTiempoInvertido(id_curso,id_std=None):
    chart = {'type': 'line'}
    dataset = []

    if id_std!=None:
        data = []
        for cuestionario in TiempoInvertidoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std):
            data.append({'x': format(cuestionario.timestamp, "%d/%m/%Y"), 'y': (cuestionario.seconds/ 60)})

        dataset.append({'data': data, 'borderColor': "#3e65cd", 'label': 'Minutos estudiante'})

    data = []
    for cuestionario in TiempoInvertidoEstudianteCursoMoodle.objects.values('timestamp').filter(curso_id=id_curso).annotate(media=Avg('seconds')).order_by('timestamp'):
        data.append({'x': format(cuestionario['timestamp'], "%d/%m/%Y"), 'y': (cuestionario['media'] / 60)})

    dataset.append({'data': data, 'borderColor': "#3e95cd", 'label': 'Minutos'})

    chart['data'] = {'datasets': dataset}
    chart['options'] = {
        'scales': {'xAxes': [{'type': 'time', 'time': {'unit': 'day', 'round': 'day', 'parser': 'D/M/YYY'}}]},
        'title': {
            'display': 'true',
            'text': 'Tiempo invertido',
            'fontSize': 16
        }
        }
    return chart



