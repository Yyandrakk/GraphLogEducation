from django.dispatch import receiver
from  django.db.models.signals import post_save
from .models import CursoMoodle
import pandas as pd

@receiver(post_save, sender=CursoMoodle)
def creacion_informacion_curso(sender,instance,created, **kwargs):
    print("ha llegado1")
    if created:
        df = pd.read_csv(instance.documento)
        print (df)
    else:
        if "documento" is kwargs.get("update_fields",False):
            print("documento")

