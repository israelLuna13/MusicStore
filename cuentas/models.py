from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class  UsuarioPers(AbstractUser):
    pass    # Añadir 'related_name' a las relaciones muchos a 