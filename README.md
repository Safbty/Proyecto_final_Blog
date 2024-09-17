# Explicacion del repo en markdown

## Proyecto final

Desarrollo de una aplicación web realizada en Django con bases de datos, específicamente un Blog orientado a promocionar noticias o
artículos.

### Funcionalidades Mínimas

* El acceso de diversos perfiles (admin, registrado, etc).
* Cargar un nuevo post, eliminar post publicados (con diversas restricciones).
* Comentar posts por parte de usuarios con perfil registrado. Un usuario debe estar autenticado y tener perfil registrado para poder comentar.
* Login a usuario tipo admin y registrado.
* Filtrar post por fecha, categoría de post y comentarios recibidos.

## ESTRUCTURA DEL PROYECTO

```text

├── entorno/      <--- Carpeta del entorno
│ ├── Scripts/
│ │ ├── activate.bat
│ │ ├── deactivate.bat
│ │ └── ...
│ └── ...
├── blog-repo/     <--- Carpeta del Repositorio
│ ├── blog/         <--- Carpeta del proyecto Django
│ │ ├── apps/     <--- Aplicaciones Django
│ │ │ ├── post/
│ │ │ │ ├── __pycache__/     **Ignorada en el .gitignore**
│ │ │ │ ├── migrations/      **Ignorada en el .gitignore**
│ │ │ │ ├── __init__.py
│ │ │ │ ├── admin.py
│ │ │ │ ├── apps.py
│ │ │ │ ├── models.py
│ │ │ │ ├── tests.py
│ │ │ │ ├── urls.py
│ │ │ │ └── views.py
│ │ │ ├── user/
│ │ │ │ ├── __pycache__/     **Ignorada en el .gitignore**
│ │ │ │ ├── migrations/      **Ignorada en el .gitignore**
│ │ │ │ ├── __init__.py
│ │ │ │ ├── admin.py
│ │ │ │ ├── apps.py
│ │ │ │ ├── models.py
│ │ │ │ ├── tests.py
│ │ │ │ ├── urls.py
│ │ │ │ └── views.py
│ │ │ └── ...
│ │ ├── blog/
│ │ │ ├── __pycache__/      **Ignorada en el .gitignore**
│ │ │ ├── configurations/     <--- Configuraciones django (opcional)
│ │ │ │ ├── __pycache__/     **Ignorada en el .gitignore**
│ │ │ │ ├── local.py      <--- Configuraciones para desarrollo local
│ │ │ │ ├── production.py     <--- Configuraciones para produccion
│ │ │ │ ├── settings.py      <--- Configuraciones base
│ │ │ │ └── ...
│ │ │ ├── __init__.py
│ │ │ ├── asgi.py
│ │ │ ├── settings.py
│ │ │ ├── urls.py
│ │ │ ├── wsgi.py
│ │ │ └── ...
│ │ ├── media/        <--- Archivos multimedia - **Podria ser ignorada en el .gitignore**
│ │ │ ├── post/
│ │ │ │ ├── post_default.jpeg
│ │ │ │ └── ...
│ │ │ ├── user/
│ │ │ │ ├── user_default.png
│ │ │ │ └── ...
│ │ │ └── ...
│ │ ├── static/        <--- Archivos estáticos
│ │ │ ├── assets/
│ │ │ │ ├── img/
│ │ │ │ ├── svg/
│ │ │ │ ├── favicon.ico
│ │ │ │ └── ...
│ │ │ ├── css/
│ │ │ │ ├── style.css
│ │ │ │ └── ...
│ │ │ ├── js/
│ │ │ │ ├── main.js
│ │ │ │ └── ...
│ │ │ └── ...
│ │ ├── templates/       <--- Archivos templates
│ │ │ ├── auth/
│ │ │ │ ├── auth_login.html
│ │ │ │ ├── auth_register.html
│ │ │ │ └── ...
│ │ │ ├── errors/
│ │ │ │ ├── not_found.html
│ │ │ │ ├── internal_error.html
│ │ │ │ └── ...
│ │ │ ├── includes/
│ │ │ │ ├── base.html
│ │ │ │ ├── footer.html
│ │ │ │ ├── header.html
│ │ │ │ └── ...
│ │ │ ├── post/
│ │ │ │ ├── post_delete.html
│ │ │ │ ├── post_detail.html
│ │ │ │ ├── post_list.html
│ │ │ │ ├── post_new.html
│ │ │ │ ├── post_update.html
│ │ │ │ └── ...
│ │ │ ├── user/
│ │ │ │ ├── user_profile.html
│ │ │ │ ├── user_update.html
│ │ │ │ └── ...
│ │ │ ├── index.html
│ │ │ └── ...
│ │ ├── db.sqlite3       <--- Base de datos - **Ignorada en el .gitignore**
│ │ ├── manage.py
│ │ └── ...
│ ├── .gitignore
│ ├── README.md        <--- Archivo README.md - Describe el proyecto
│ ├── requeriments.txt      <--- Archivo requeriments.txt - Enlista los paquetes
| └── ...
└── ...
```
