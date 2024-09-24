# blog_django/blog_django/configurations/base.py
from pathlib import Path
import os
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Define la ruta base del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!

# Define la clave secreta de la aplicación.

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
#Clave de mi archivo
SECRET_KEY = os.getenv('SECRET_KEY')


#ALLOWED_HOSTS = ("localhost")


# Application definition
# Define las aplicaciones instaladas en el proyecto.
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'apps.post',
'apps.user',
]


# Middleware configuration
# Define los middleware que se aplicarán a las solicitudes y respuestas de la aplicación.
# Los middleware son una serie de hooks o ganchos que se ejecutan antes o después de una vista.
MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Define la URL raíz de la aplicación.
ROOT_URLCONF = 'blog_django.urls'
TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [os.path.join(BASE_DIR, 'templates')],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
},
]

WSGI_APPLICATION = 'blog_django.wsgi.application'
# Database settings will be set in local/production
# Password validation
# Define las validaciones que se aplicarán a las contraseñas de los usuarios.
AUTH_PASSWORD_VALIDATORS = [
{
'NAME':
'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
},
{
'NAME':
'django.contrib.auth.password_validation.NumericPasswordValidator',
},
]

# Internationalization
LANGUAGE_CODE = 'es-ar'
# Define la zona horaria predeterminada.
TIME_ZONE = 'America/Argentina/Buenos_Aires'
# Define si se activa o no la traducción de los textos de la aplicación.
USE_I18N = True
# Define si se activa o no el uso de la zona horaria.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# En desarrollo y producción:
# Define el prefijo de URL para los archivos estáticos.
# Al hacer referencia a archivos estáticos en las plantillas, Django buscará los archivos en esta ruta.
STATIC_URL = '/static/'
# STATICFILES_DIRS: Se usa principalmente en desarrollo para decirle a Django
# dónde encontrar archivos estáticos adicionales.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT: Es necesario para producción y define dónde se guardarán todos los archivos estáticos después de ejecutar collectstatic.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# URL base para acceder a los archivos subidos por los usuarios
# Seguridad: Asegurarse de validar los tipos de archivo permitidos y aplicar
# otras medidas de seguridad para evitar que se suban archivos maliciosos.
# Por supuesto se podria considerar usar un servicio de almacenamiento en la nube como AWS S3.


MEDIA_URL = '/media/'
# Directorio donde se almacenarán los archivos subidos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/es/5.1/ref/settings/#default-auto-field
# Define el tipo de campo de clave primaria que se utilizará para todos los modelos de Django.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#TODO CAMBIAR CONFIGURACIONES DE SEGURIDAD
#TODO CAMBIAR EN A LANG= ES-AR

"""
# blog_django/blog_django/configurations/base.py
SECRET_KEY = os.getenv(
'SECRET_KEY', 'django-insecure-r*bw(
fop+@8e$85lzqh#_o1*ueh_5_v*9i^5tqztl56uj8bj4')
# 1- Eliminar la clave secreta del historial del repositorio
# Este comando eliminará el archivo settings.py del historial de Git.
# Posteriormente, deberiamos volver a agregar el archivo sin la clave secreta.
git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch blog_django/settings.py" \
--prune-empty --tag-name-filter cat -- --all
# Luego pushear los cambios y forzarlos en el repositorio remoto ya que se ha
modificado la historia.
git push origin --force --all
# 2- Regenerar una clave secreta desde la terminal con el comando
python -c 'from django.core.management.utils import get_random_secret_key;
print(get_random_secret_key())'
# 3- Definir la clave secreta al archivo .env
SECRET_KEY='nueva_clave_secreta_generada'
# 4- Actualizar el archivo base.py para que solo contenga la definición de la
clave secreta
SECRET_KEY = os.getenv('SECRET_KEY')
# No es obligatorio eliminar la clave anterior del repositorio, pero es muy
recomendable para prevenir futuras vulnerabilidades si la aplicacion ya se .
# Cambiar la clave secreta no invalida la anterior automáticamente, por lo que se
deben tomar medidas adicionales (como limpiar sesiones [python manage.py
clearsessions]) para proteger la aplicación.
"""

#Configuracion para usar el nuevo modelo user
AUTH_USER_MODEL = 'user.User'

