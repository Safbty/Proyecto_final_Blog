# blog_django/apps/post/urls.py
from django.urls import path
import apps.post.views as views
from .views import UserPostView
app_name = 'post'

urlpatterns = [
# Como cada post tiene un uuid, deberiamos usar un slug en lugar de el uuid como parametro
# Un slug es una cadena de texto que identifica de manera unica un recurso
# Pero a diferencia de un uuid, un slug es mas facil de recordar y de escribir
# En este caso, un post podria tener un slug que sea el titulo del post

# path('post/<str:slug>/', views.post_detail, name='post_detail'),
# path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('posts/', views.PostListView.as_view(), name="post_list"),
    path('posts/create', views.PostCreateView.as_view(), name="post_create"),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(),
    name="post_detail"),
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(),
    name="post_update"),
    path('posts/<slug:slug>/delete', views.PostDeleteView.as_view(),
    name="post_delete"),
    path('posts/<slug:slug>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<uuid:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('user/', UserPostView.as_view(), name='user_posts'),  # Nueva URL para posts de un usuario
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'), #Urls para categorias vistas
    path('categories/<uuid:id>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<uuid:id>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('movies/', views.movie_list_view, name='movie_list'),  #ruta de movie_list
]


"""
post_list: URL para listar los posts.
post_create: URL para crear un nuevo post.
post_detail: URL para ver un post en detalle.
post_update: URL para actualizar un post.
post_delete: URL para eliminar un post.
"""

#TODO: en admin, crear post

"""
Nota: La URL para editar un comentario se define como //. El parámetro pk se utiliza para identificar el
comentario que se desea editar.
La URL comment_update espera el pk del comentario y apunta a la vista CommentUpdateView.
Importante: El parámetro pk es un campo UUID que se utiliza para identificar de forma única un
comentario.
"""
