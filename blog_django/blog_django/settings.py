# blog_django/blog_django/settings.py
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

DJANGO_ENV = os.getenv('DJANGO_ENV', 'development') #'development' por defecto

if DJANGO_ENV == 'production':
    from .configurations.production import *
else:
    from .configurations.local import *
    