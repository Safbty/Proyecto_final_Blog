# blog_django/apps/post/apps.py
from django.apps import AppConfig

class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.post'

    def ready(self):
        import  apps.post.signals  # noqa: F401
