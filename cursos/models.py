from django.db import models
# Create your models here.


class AbstractCurso(models.Model):
    profesor = models.ForeignKey('usuarios.Usuario',on_delete = models.CASCADE)
    nombre = models.CharField(max_length=50,null=False,blank=False)
    desc = models.TextField(max_length=200)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CursoMoodle(AbstractCurso):
    umbral = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["-actualizado"]
        unique_together = ["profesor", "nombre"]