from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
import os


# Create your models here.
class Post(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable= False)
    title= models.CharField(max_length=200)
    slug= models.SlugField(unique = True, max_length=200, blank= True)
    content= models.TextField(max_length=10000)
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    creation_date= models.DateTimeField(default=timezone.now)
    modification_date= models.DateField(auto_now= True)
    allow_comments= models.BooleanField(default= True)

    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, related_name='posts')


    def __str__(self):
        return self.title
    
    @property
    #TODO definir comments
    def amount_comments(self):
        return self.comments.count()

    @property
    #TODO definir imagenes
    def amount_images(self):
        return self.images.count()


    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
        
        if not self.images.exists():
            PostImage.objects.create(post=self, image='post/default/post_default.png')

        #TODO definir imagenes portada
    
    def generate_unique_slug(self):
        #tenemos este titulo par el post 1
        #tenemos-este-titulo-para-el-post-1  ----> para no dejar espacio en las urls
        slug = slugify(self.title)
        unique_slug = slug
        num = 1

        while Post.objects.filter(slug= unique_slug).exists():
            unique_slug=  f"{slug}-{num}"
            num += 1

        return unique_slug    


# blog_django/apps/post/models.py
def get_image_filename(instance, filename):
    post_id = instance.post.id
    images_count = instance.post.images.count()
    base_filename, file_extension = os.path.splitext(filename) # esto se llama unpacking (desempaquetado)
    new_filename = f"post_{post_id}_cover_{images_count + 1}{file_extension}"
    return os.path.join('post/cover/', new_filename)

class PostImage (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename, default='post/default/post_default.png')
    active =  models.BooleanField(default=True)



    def __str__(self):
        return f"PostImage {self.id}"

#TODO imagen cover.png default post en carpeta cover
#Imagen de avatar en .png
#TODO realizar migraciones(tabla post image)



#TODO crear nueva app comnetarios para definirlos a parte
#TODO definir portada (portrait image_file)

class Comment(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable= False)
    content= models.TextField(max_length=500)
    creation_date= models.DateTimeField(auto_now_add=True)
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    post= models.ForeignKey(Post, on_delete= models.CASCADE, related_name="comments")

    #TODO terminar de definir funcion
    def __str__(self):
        return self.content
    

class Category (models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='category_posts')