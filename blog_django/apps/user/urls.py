# blog_django/apps/user/urls.py
from django.urls import path
import apps.user.views as views
app_name = 'user'
urlpatterns = [
path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),
]