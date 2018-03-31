from datetime import datetime

from django.db.models import Sum
from cursos.models import TiempoDedicadoCursoMoodle, TiempoDedicadoEstudianteCursoMoodle
from django.db.models.functions import ExtractWeek, ExtractYear


def graficaTiempo(id_curso, id_std=None):
    chart = {'type': 'line'}
    dataset = []
    if id_std!=None:
        dias = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD)
        count = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD).aggregate(
            total=Sum('contador'))
        data = []
        for dia in dias:
            data.append({'x':format(dia.timestamp, "%d/%m/%Y"),'y':((dia.contador / count['total']) * 100)})
        dataset.append({'data': data, 'borderColor': "#3e65cd", 'label': 'Eventos estudiante'})

    dias = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA)
    count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(
            total=Sum('contador'))
    data = []
    for dia in dias:
       data.append({'x':format(dia.timestamp, "%d/%m/%Y"),'y':((dia.contador / count['total']) * 100)})

    dataset.append({'data': data, 'borderColor': "#3e95cd", 'label': 'Eventos general'})
    chart['data'] = {'datasets': dataset}
    chart['options'] = {'scales': {'xAxes':[{'type':'time','time':{'unit':'day','round':'day','parser':'D/M/YYY'} }]}}

    return chart


def graficaTiempoSemanal(id_curso, id_std=None):
    chart = {'type': 'line'}
    dataset = []
    data = []

    if id_std != None:
        semanas = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std, tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD).annotate(
            week=ExtractWeek('timestamp')).values('week').annotate(s=Sum('contador')).values('week', 's').annotate(anyo=ExtractYear('timestamp')).values('week','anyo', 's').order_by('week')
        count = TiempoDedicadoEstudianteCursoMoodle.objects.filter(curso_id=id_curso,estudiante_id=id_std,
                                                         tipo=TiempoDedicadoEstudianteCursoMoodle.DIA_STD).aggregate(total=Sum('contador'))
        for semana in semanas:
            data.append({'x': datetime.strptime(str(semana['anyo']) + ' ' + str(semana['week']) + ' 1',"%Y %W %w").strftime("%d/%m/%Y"),'y': ((semana['s'] / count['total']) * 100)})
        dataset.append({'data': data, 'borderColor': "#3e65cd", 'label': 'Eventos estudiante'})


    count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(
        total=Sum('contador'))
    semanas = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).annotate(
        week=ExtractWeek('timestamp')).values('week').annotate(s=Sum('contador')).values('week', 's').annotate(anyo=ExtractYear('timestamp')).values('week','anyo', 's').order_by('week')
    data = []
    for semana in semanas:
        data.append({'x':datetime.strptime(str(semana['anyo']) +' ' + str(semana['week']) + ' 1', "%Y %W %w").strftime("%d/%m/%Y"),'y':((semana['s'] / count['total']) * 100)})

    dataset.append({'data': data, 'borderColor': "#3e95cd", 'label': 'Eventos general'})
    chart['data'] = {'datasets': dataset}

    chart['options'] = {'scales': {'xAxes': [{'type': 'time', 'time': {'unit': 'day', 'round': 'day', 'parser': 'D/M/YYY'}}]}}

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
                                                          "#18FFAD"], 'label': 'Eventos estudiante'})

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
                                                     "#18FFAD"], 'label': 'Eventos'})

    chart['data'] = {'labels': labels, 'datasets': dataset}
    return chart




