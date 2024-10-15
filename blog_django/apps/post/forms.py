from django import forms
from apps.post.models import Post, PostImage, Comment, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'allow_comments', 'category')


#TODO ver porque imgen default se manteinen cuando ya se cargó una imagen para el post (cambiar sistema CHECKBOX)

class NewPostForm(PostForm):
    image = forms.ImageField(required=False)

    def save(self, commit=True):
        # Guardar el post pero no aún en la base de datos ya que necesitamos el id del post para la imagen
        post = super().save(commit=False)
        image = self.cleaned_data['image']

        if commit:
            post.save()  # Guardar el post
            if self.cleaned_data['image']:
                PostImage.objects.create(
                    # Creamos la imagen
                    post=post, image=self.cleaned_data['image'])
        return post




class UpdatePostForm(PostForm):
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        # Obtenemos las imágenes activas del post que se quiere actualizar
        self.active_images = kwargs.pop('active_images', None)
        super(UpdatePostForm, self).__init__(*args, **kwargs)

        if self.active_images:
            for image in self.active_images:
                # keep_image_1, keep_image_2, ... etc es el nombre del campo que se creará en el formulario para mantener la imagen activa
                field_name = f"keep_image_{image.id}"
                self.fields[field_name] = forms.BooleanField(
                    required=False, initial=True, label=f"Mantener {image}")

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()
            if self.cleaned_data['image']:  # Si el usuario sube una nueva imagen
                PostImage.objects.create(post=post, image=self.cleaned_data['image'])

            if self.active_images:  # Si hay imágenes activas y se quiere mantener alguna
                for image in self.active_images:
                    # Eliminar la imagen si el usuario no la quiere mantener, checkboxes desmarcados
                    if not self.cleaned_data.get(
                        f"keep_image_{image.id}", True): image.delete()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
        labels = {
            'content': 'Comentario'
        }
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario...', 'class': 'p-2'})
        }

class PostFilterForm(forms.Form):
    search_query = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar...', 'class': 'w-fullp-2'})
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=(
            ('-creation_date', 'Más reciente'),
            ('creation_date', 'Más antiguo'),
            ('-comments_count', 'Más comentado'),
        ),
        widget=forms.Select(attrs={'class': 'w-full p-2'})
    )        

#FILTRO CATEGORIA LISTADO
class MovieFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Selecciona un género",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


#TODO: formulario category

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        labels = {
        'Title': 'Nueva Categoria'
        }
        
        widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Agregar nueva categoria', 'class': 'form-control p-2'})
        }  




#En este formulario, definimos el formulario UpdatePostForm que hereda de PostForm y agrega un campo image de tipo forms.ImageField.

# Definimos el método __init__ para obtener las imágenes activas del post que se quiere actualizar y crear un campo en el formulario para mantener la imagen activa.

# Definimos el método save para guardar el post y las imágenes, y eliminar las imágenes que el usuario no quiere mantener.

# Nota: Para poder mantener las imágenes activas, es necesario definir un campo active de tipo BooleanField en el modelo PostImage que nos permita saber si la imagen esta activa o no.

#El formulario PostFilterForm tiene dos campos:
# search_query: Lo definimos un campo de texto que permite buscar posts por título o autor.
# order_by: Lo definimos un campo select que permite ordenar los posts por fecha de creación o cantidad de comentarios.
# Ambos campos son opcionales (required=False), ya que no es obligatorio completarlos, y están diseñados con clases de TailwindCSS.
