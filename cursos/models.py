from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/curso_{1}/{2}'.format(instance.profesor.id, instance.nombre, filename)

class AbstractCurso(models.Model):
    profesor = models.ForeignKey(get_user_model(),on_delete = models.CASCADE)
    nombre = models.CharField(max_length=50,null=False,blank=False)
    desc = models.TextField(max_length=200)
    actualizado = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    class Meta:
        abstract = True


class CursoMoodle(AbstractCurso):
    umbral = models.PositiveSmallIntegerField()
    documento = models.FileField(upload_to=user_directory_path,validators=[FileExtensionValidator(['csv'])])
    procesado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-actualizado"]
        unique_together = ["profesor", "nombre"]


class EstudianteCursoMoodle(models.Model):
    curso = models.ForeignKey(CursoMoodle,on_delete = models.CASCADE)
    nombre = models.CharField(max_length=100,null=False,blank=False)


class MaterialCursoMoodle(models.Model):
    ARCHIVO = 'AR'
    CUESTIONARIO = 'CU'
    TYPES = ((ARCHIVO,"Archivo"), (CUESTIONARIO,"Fichero"))
    curso = models.ForeignKey(CursoMoodle,on_delete = models.CASCADE)
    nombre = models.CharField(max_length=100,null=False,blank=False)
    tipo = models.CharField(max_length=2,choices=TYPES,null=False)
    contador = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ["curso", "nombre","tipo"]


class TiempoDedicadoCursoMoodle(models.Model):
    DIA = 'DI'
    HORA = 'HO'
    TYPES = ((DIA,"Dia"), (HORA, "Hora"))
    curso = models.ForeignKey(CursoMoodle, on_delete=models.CASCADE)
    contador = models.IntegerField(null=False,blank=False)
    tipo = models.CharField(max_length=2, choices=TYPES, null=False)
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ["curso", "timestamp","tipo"]


class TiempoDedicadoEstudianteCursoMoodle(models.Model):
    DIA_STD = "DS"
    HORA_STD = "HS"
    TYPES_STD = ((DIA_STD,"Dia estudiante"),(HORA_STD,"Hora estudiante"))
    curso = models.ForeignKey(CursoMoodle, on_delete=models.CASCADE)
    contador = models.IntegerField(null=False,blank=False)
    tipo = models.CharField(max_length=2, choices=TYPES_STD, null=False)
    timestamp = models.DateTimeField()
    estudiante = models.ForeignKey(EstudianteCursoMoodle,on_delete=models.CASCADE,blank = True,null=True)

    class Meta:
        unique_together = ["curso", "timestamp", "tipo", "estudiante"]


class TiempoInvertidoEstudianteCursoMoodle(models.Model):
    curso = models.ForeignKey(CursoMoodle, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(EstudianteCursoMoodle, on_delete=models.CASCADE,  blank=False, null=False)
    timestamp = models.DateTimeField()
    seconds = models.IntegerField(null=False, blank=False)


class TiempoInvertidoMaterialCursoMoodle(models.Model):
    curso = models.ForeignKey(CursoMoodle, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(EstudianteCursoMoodle, on_delete=models.CASCADE,  blank=False, null=False)
    seconds = models.IntegerField(null=False, blank=False)
    contexto = models.ForeignKey(MaterialCursoMoodle, on_delete=models.CASCADE,  blank=True, null=True)