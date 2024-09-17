# blog_django/apps/post/urls.py
from django.urls import path
import apps.post.views as views
app_name = 'post'

urlpatterns = [
# Como cada post tiene un uuid, deberiamos usar un slug en lugar de el uuid como parametro
# Un slug es una cadena de texto que identifica de manera unica un recurso
# Pero a diferencia de un uuid, un slug es mas facil de recordar y de escribir
# En este caso, un post podria tener un slug que sea el titulo del post
# TODO: Cambiar paara recibir un parametro de tipo <slug:slug>
path('posts/<slug:slug>/', views.PostDetailView.as_view(),
name='post_detail'),
]