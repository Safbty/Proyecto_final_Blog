
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from blog_django.views import IndexView, not_found_view, internal_error_view, forbidden_view
from django.contrib.auth import views as auth_views

#from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('', include('apps.user.urls')),
    path('', include('apps.post.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Manejadores de errores

handler404 = not_found_view
handler500 = internal_error_view
handler403 = forbidden_view

# Los manejadores estan disponibles en cualquier parte de la aplicación,
# por lo que no es necesario importarlos en cada vista.
# o incluso aqui en blog\blog\urls.py

if settings.DEBUG:
    from django.conf.urls.static import static
    # Sirviendo archivos estáticos
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Sirviendo archivos media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Nota: Los handlers de errores se definen y asocian a las vistas que renderizan los templates personalizados que creamos anteriormente.

