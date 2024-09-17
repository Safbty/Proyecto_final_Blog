from django.shortcuts import render

# Create your views here.

# blog_django/apps/post/views.py
from django.views.generic import TemplateView
# TODO: Cambiar TemplateView por DetailView para que se pueda ver el detalle de un post
class PostDetailView(TemplateView):
    template_name = 'post/post_detail.html'