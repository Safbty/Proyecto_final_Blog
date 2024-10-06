
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


class User(AbstractUser):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to= get_avatar_filename, default= "user/default/avatar_default.jpg")

    @property
    def is_collaborator(self):
        return self.groups.filter(name='Collaborators').exists()
    
    @property
    def is_admin(self):
        return self.groups.filter(name='Admins').exists()
    
    @property
    def is_registered(self):
        return self.groups.filter(name='Registered').exists()
    


#Nota:

#Para poder definir estas propiedades, es necesario definir los grupos Collaborators, Admins y Registered en el panel de administración de Django, o mediante un signal en el archivo signals.py de la app User, como lo hicimos en clases anteriores.

#El decorador @property nos permite definir un método como una propiedad, de manera que podamos acceder a ella como si fuera un atributo.