from apps.user.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.post.models import Post, Comment
from django.contrib.contenttypes.models import ContentType
from  django.contrib.auth.models import Permission, Group


@receiver(post_save, sender= User)
def create_groups_and_permissions(sender, instance,created, **kwargs):
    if created and instance.is_superuser:
        try:
            #TODO crear otros condicionales if  
            post_content_type= ContentType.objects.get_for_model(Post)
            comment_content_type= ContentType.objects.get_for_model(Comment)

            #Permisos POST
            view_post_permission= Permission.objects.get(codename="view_post", content_type= post_content_type)

            add_post_permission=  Permission.objects.get(codename="add_post", content_type= post_content_type)

            change_post_permission=  Permission.objects.get(codename="change_post", content_type= post_content_type)

            delete_post_permission=  Permission.objects.get(codename="delete_post", content_type= post_content_type)

            #Permisos COMENTARIOS
            view_comment_permission = Permission.objects.get(codename="view_comment", content_type=comment_content_type)
            
            add_comment_permission = Permission.objects.get(codename="add_comment", content_type=comment_content_type)
            
            change_comment_permission = Permission.objects.get(codename="change_comment", content_type=comment_content_type)
            
            delete_comment_permission = Permission.objects.get(codename="delete_comment", content_type=comment_content_type)


            # Crear grupo usuarios registrados
            registered_group, created = Group.objects.get_or_create(name='Registered')
            registered_group.permissions.add(
                view_post_permission,
                add_post_permission,
                change_post_permission,
                delete_post_permission,
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission,
            )

            # Crear grupo colaboradores
            registered_group, created = Group.objects.get_or_create(name='Collaborators')
            registered_group.permissions.add(
                view_post_permission,
                add_post_permission,
                change_post_permission,
                delete_post_permission,
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission,
                )

            #Crear grupo usuarios administradores (todos los permisos)
            registered_group, created = Group.objects.get_or_create(name='Admins')
            registered_group.permissions.set(Permission.objects.all())

            print("Se crearon los grupos y permisos")
            
        except ContentType.DoesNotExist:
            print('El tipo de conetenido aun no esta disponible.')
        except Permission.DoesNotExist:
            print('Uno o mas permisio no estan disponible aun.')



#TODO:  Crear un grupo para los colaboradores y asignarle los permisos correspondientes
#TODO:  Crear un grupo para los usuarios registrados y asignarle los permisos
#TODO: Crear  un grupo para los administradores y asignarle todos los permisos

#Grupos en bdd
    #collaborators
    #registered
    #admins

"""
# Visitante: Solo puede ver posts y comentarios.
# Usuario registrado: Puede ver, crear, editar y eliminar posts y comentarios.
# Colaborador: Tiene los mismos permisos que el usuario registrado, con posibilidad de escalar en el futuro.
# Admin: Tiene todos los permisos disponibles.
"""


#TODO: realizar migraciones de models comments y post
#TODO: crear nuevo superusuario (se elimina al borrar la base de datos)
