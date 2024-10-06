# blog_django/apps/post/views.py

from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from apps.post.models import Post, PostImage
from apps.post.forms import NewPostForm, UpdatePostForm
from django.urls import reverse, reverse_lazy
from django.conf import settings

# TODO: Cambiar TemplateView por DetailView para que se pueda ver el detalle de un post

class PostListView(ListView):
    model =  Post
    template_name = 'post/post_list.html'
    context_object_name=  'posts'



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

