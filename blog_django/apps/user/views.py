from django.shortcuts import render

# Create your views here.

# blog_django/apps/user/views.py
from django.views.generic import TemplateView
# TODO: Cambiar TemplateView por DetailView para que se pueda ver el detalle de un perfil de usuario
class UserProfileView(TemplateView):
    template_name = 'user/user_profile.html'