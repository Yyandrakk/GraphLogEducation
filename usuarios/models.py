from django.contrib.auth.models import AbstractUser


# Create your models here.

class Usuario(AbstractUser):

    def save(self,*args,**kwargs):
        return super().save(*args,**kwargs)