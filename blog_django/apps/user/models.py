#from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
import os
import uuid

#imagen3121212.png
def get_avatar_filename(instance, filename):
    #imagen3121212     #.png        #imagen3121212.png
    base_filename, file_extension= os.path.splittext(filename)
    #user_1_avatar.png
    new_filename = f"user_{instance.id}_avatar{file_extension}"
    #user/avatar/user_1_avatar.png
    return os.path.join ("user/avatar/", new_filename)

#TODO agregar archivos de imagenes default en carpeta default (usuario, imagen de post, flavicon)

class User(AbstractUser):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to= get_avatar_filename, default= "user/default/avatar_default.jpg")

#TODO desconectar bdd en dbeaver y eliminar carpeta db.sqlite en vscode, luego activar entorno y realizar migraciones (editar base.py)