# blog_django/apps/post/urls.py
from django.urls import path
import apps.post.views as views
app_name = 'post'

urlpatterns = [
# Como cada post tiene un uuid, deberiamos usar un slug en lugar de el uuid como parametro
# Un slug es una cadena de texto que identifica de manera unica un recurso
# Pero a diferencia de un uuid, un slug es mas facil de recordar y de escribir
# En este caso, un post podria tener un slug que sea el titulo del post
# TODO: Cambiar para recibir un parametro de tipo <slug:slug>
    path('posts/', views.PostListView.as_view(), name="post_list"),
    path('posts/create', views.PostCreateView.as_view(), name="post_create"),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(),
    name="post_detail"),
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(),
    name="post_update"),
    path('posts/<slug:slug>/delete', views.PostDeleteView.as_view(),
    name="post_delete"),
]

"""
post_list: URL para listar los posts.
post_create: URL para crear un nuevo post.
post_detail: URL para ver un post en detalle.
post_update: URL para actualizar un post.
post_delete: URL para eliminar un post.
"""

#TODO: en admin, crear post
