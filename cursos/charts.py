import datetime

from django.db.models import Sum



from cursos.models import TiempoDedicadoCursoMoodle, TiempoDedicadoEstudianteCursoMoodle


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