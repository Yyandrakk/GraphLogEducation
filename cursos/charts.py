
from django.db.models import Sum
from cursos.models import TiempoDedicadoCursoMoodle, TiempoDedicadoEstudianteCursoMoodle
from django.db.models.functions import ExtractWeek


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
    labels = []
    data = []

    if id_std != None:
        semanas=[]

    count = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).aggregate(
        total=Sum('contador'))
    semanas = TiempoDedicadoCursoMoodle.objects.filter(curso_id=id_curso, tipo=TiempoDedicadoCursoMoodle.DIA).annotate(
        week=ExtractWeek('timestamp')).values('week').annotate(s=Sum('contador')).values('week', 's').order_by('week')
    for semana in semanas:
        labels.append(semana['week'])
        data.append((semana['s'] / count['total']) * 100)
    chart['data'] = {'labels': labels, 'datasets': [{'data': data, 'borderColor': "#3e95cd", 'label': 'Eventos'}]}

    return chart

