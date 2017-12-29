import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Usuario(AbstractUser):
    token = models.CharField(max_length=40)

    def save(self,*args,**kwargs):

        if not self.token:
            self.token = binascii.hexlify(os.urandom(30)).decode()
        return super().save(*args,**kwargs)