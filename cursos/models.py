from django.core.validators import FileExtensionValidator
from django.db import models
# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/curso_{1}/{2}'.format(instance.profesor.id, instance.nombre, filename)

class AbstractCurso(models.Model):
    profesor = models.ForeignKey('usuarios.Usuario',on_delete = models.CASCADE)
    nombre = models.CharField(max_length=50,null=False,blank=False)
    desc = models.TextField(max_length=200)
    actualizado = models.DateTimeField(auto_now=True)
    slug = models.SlugField(populate_from='nombre',unique_with=('profesor__id', 'nombre'))

    class Meta:
        abstract = True


class CursoMoodle(AbstractCurso):
    umbral = models.PositiveSmallIntegerField()
    documento = models.FileField(upload_to=user_directory_path,validators=[FileExtensionValidator(['csv'])])
    procesado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-actualizado"]
        unique_together = ["profesor", "nombre"]

