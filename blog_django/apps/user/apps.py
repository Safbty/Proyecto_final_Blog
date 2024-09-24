# blog_django/apps/user/apps.py
from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'
    
    # Agregamos aqui el metodo para que se ejecuten los signals

    def ready(self):
        import  apps.user.signals

