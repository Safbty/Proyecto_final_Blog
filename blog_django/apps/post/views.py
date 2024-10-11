# blog_django/apps/post/views.py

from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from apps.post.forms import NewPostForm, UpdatePostForm, CommentForm, PostFilterForm
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.post.models import Comment, Post, PostImage
from django.db.models import Count


class PostListView(ListView):
    model =  Post
    template_name = 'post/post_list.html'
    context_object_name=  'posts'
    paginate_by = 10 # Definimos la paginación de 10 posts por página
    
    def get_queryset(self):
        queryset = Post.objects.all().annotate(comments_count=Count('comments'))
        # Anotamos la cantidad de comentarios en cada post
        
        search_query = self.request.GET.get('search_query', '')
        order_by = self.request.GET.get('order_by', '-creation_date')
        
        # Filtramos por título o autor si se proporciona una búsqueda
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) |queryset.filter(author__username__icontains=search_query)
            
        return queryset.order_by(order_by)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PostFilterForm(self.request.GET) # Pasamos el formulario de filtro al contexto
        
        # Manejamos la paginación
        if context.get('is_paginated', False):
            query_params = self.request.GET.copy()
            query_params.pop('page', None)
            
            pagination = {}
            page_obj = context['page_obj']
            paginator = context['paginator']
            
            # Usamos number para obtener el número de la página actual
            if page_obj.number > 1:
                pagination['first_page'] = f'?{query_params.urlencode()}&page={paginator.page_range[0]}'
            
            # Usamos has_previous para saber si hay una página anterior
            if page_obj.has_previous():
                pagination['previous_page'] = f'?{query_params.urlencode()}&page={page_obj.number - 1}'
                
            # Usamos has_next para saber si hay una página siguiente
            if page_obj.has_next():
                pagination['next_page'] = f'?{query_params.urlencode()}&page={page_obj.number + 1}'
                
            # Usamos num_pages para obtener el número total de páginas
            if page_obj.number < paginator.num_pages:
                pagination['last_page'] = f'?{query_params.urlencode()}&page={paginator.num_pages}'
                
            context['pagination'] = pagination
            
        return context
    
"""
El método get_queryset obtiene los posts y los anota con la cantidad de comentarios. Luego aplica los filtros basados en la búsqueda (search_query) y el criterio de orden (order_by).
El método get_context_data agrega el formulario de filtro al contexto y maneja la lógica de paginación, creando enlaces para navegar entre páginas.
"""

class PostCreateView(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'post/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        
        images = self.request.FILES.getlist('images')
        
        if images:
            for image in images:
                PostImage.objects.create(post=post, image=image)
        else:
            PostImage.objects.create(post=post, image=settings.DEFAULT_POST_IMAGE)
            
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.object.slug})


class PostDetailView(DetailView):
    template_name = 'post/post_detail.html'
    model = Post
    context_object_name = 'post'

    #Nota: Para poder obtener las imágenes del post, es necesario definir una relación ForeignKey en el modelo PostImage que haga referencia al modelo Post y un campo active que nos permita saber si la imagen esta activa o no, en este caso, se ha definido un campo active de tipo BooleanField en el modelo PostImage. Ademas podemos acceder a través de self.object.images ya que hemos definido una relación related_name='images' en el modelo PostImage.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todas las imagenes activas del post
        active_images = self.object.images.filter(active= True)

        context['active_images'] = active_images
        context['add_comment_form'] = CommentForm()

        # Editar comentario
        edit_comment_id = self.request.GET.get('edit_comment')
        if edit_comment_id:
            comment = get_object_or_404(Comment, id=edit_comment_id)
            # Permitimos editar solo si el usuario logueado es el autor del comentario
            if comment.author == self.request.user:
                context['editing_comment_id'] = comment.id
                context['edit_comment_form'] = CommentForm(instance=comment)
            else:
                context['editing_comment_id'] = None
                context['edit_comment_form'] = None

        # Eliminar comentario
        delete_comment_id = self.request.GET.get('delete_comment')
        if delete_comment_id:
            comment = get_object_or_404(Comment, id=delete_comment_id)
            # Permitimos solo si el usuario logueado tiene permiso para eliminar el comentario
            if (
                # Es autor del comentario
                comment.author == self.request.user or
                # Es autor del post, pero el comentario no es de un admin o un superuser
                (comment.post.author == self.request.user and not comment.author.is_admin and not comment.author.is_superuser) or
                self.request.user.is_superuser or # Es Superuser
                self.request.user.groups.filter(name='Admins').exists() # Es Admin
            ):
                context['deleting_comment_id'] = comment.id
            else:
                context['deleting_comment_id'] = None

        return context
    
    
    
class PostUpdateView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'post/post_update.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['active_images'] = self.get_object().images.filter(active=True) # Pasamos las imágenes activas
        return kwargs
    
    def form_valid(self, form):
        post = form.save(commit=False)
        active_images = form.active_images
        keep_any_image_active = False
        
        # Manejo de las imágenes activas
        if active_images:
            for image in active_images:
                field_name = f"keep_image_{image.id}"
                # Si el checkbox no está marcado, eliminamos la imagen
                if not form.cleaned_data.get(field_name, True):
                    image.active = False
                    image.save()
                else:
                    keep_any_image_active = True
                    
        # Manejo de las nuevas imágenes subidas
        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                PostImage.objects.create(post=post, image=image)
        # Si no se desea mantener ninguna imagen activa y no se subieron nuevas imágenes, se agrega una imagen por defecto
        
        if not keep_any_image_active and not images:
            PostImage.objects.create(post=post, image=settings.DEFAULT_POST_IMAGE)
        post.save() # Guardar el post finalmente
        return super().form_valid(form)
    
    def get_success_url(self):
        # El reverse_lazy es para que no se ejecute hasta que se haya guardado el post
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.slug})


class PostDeleteView(DeleteView):
    template_name = 'post/post_delete.html'
    model = Post
    success_url = reverse_lazy('post:post_list') # Redirecciona a la url
    # definida en el archivo urls.py con el nombre post_list


#mportante: En el método form_valid, se manejan las imágenes activas y las nuevas imágenes subidas por el usuario, y se guarda el post finalmente.

#COMENTARIOS

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'
    login_url = reverse_lazy('user:auth_login')
    
    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})
    
    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    login_url = reverse_lazy('user:auth_login')
    
    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})
    
    def test_func(self):
        comment = self.get_object()
        
        is_comment_author = self.request.user == comment.author
        
        is_post_author = (
            self.request.user == comment.post.author and
            not comment.author.is_admin and
            not comment.author.is_superuser
        )
        
        is_admin = self.request.user.is_superuser or self.request.user.groups.filter (name='Admins').exists()
        return is_comment_author or is_post_author or is_admin



#TODO Validar las vistas de cada clase con login required

#TODO Validar que el usuario que está editando o borrando sea el autor del post
#TODO Validar que el usuario que está editando o borrando sea el autor del comentario

"""
La vista CommentCreateView hereda de CreateView y se encarga de gestionar la creación de un nuevo comentario.
El método form_valid asigna el autor del comentario como el usuario autenticado y relaciona el comentario con el post actual.
El método get_success_url redirige a la vista de detalle del post una vez que el comentario se ha creado.
"""

"""
La vista CommentUpdateView hereda de UpdateView de Django que permite actualizar un objeto
existente, en este caso, un comentario. Se utiliza el formulario CommentForm para editar el contenido
del comentario.
Definimos la variable login_url para redirigir al usuario a la página de inicio de sesión si no está
autenticado.
El método get_object se encarga de obtener el comentario que se desea editar. Utilizamos el
parámetro pk para identificar el comentario que se desea editar.
El método get_success_url redirige a la vista de detalle del post una vez que el comentario se ha
editado.
Utilizamos el método test_func para verificar si el usuario autenticado es el autor del comentario.
Solo el autor del comentario puede editar su propio comentario. Caso contrario se redirigira a una
página de error 403.
"""

"""
La vista CommentDeleteView hereda de DeleteView de Django que permite eliminar un objeto
existente, en este caso, un comentario.
Definimos la variable login_url para redirigir al usuario a la página de inicio de sesión si no está
autenticado.
El método get_object se encarga de obtener el comentario que se desea eliminar. Utilizamos el
parámetro pk para identificar el comentario que se desea eliminar.
El método get_success_url redirige a la vista de detalle del post una vez que el comentario se ha
eliminado.
Utilizamos el método test_func para verificar si el usuario autenticado es el autor del comentario, el
autor del post o un administrador. Solo el autor del comentario, el autor del post o un administrador
pueden eliminar un comentario. Caso contrario se redirigira a una página de error 403.
Solo los usuarios autenticados pueden eliminar sus propios comentarios. Solo el colaborador autor del
post o un administrador pueden eliminar cualquier comentario.
"""

"""
Nota: En la vista PostDetailView, agregamos la lógica para mostrar un formulario de confirmación de
eliminación de comentarios.
Si el usuario autenticado es el autor del comentario, el autor del post, un administrador o un
superusuario, se muestra un formulario de confirmación de eliminación.
Si el usuario autenticado no tiene permiso para eliminar el comentario, no se muestra el formulario de
confirmación de eliminación.
"""
