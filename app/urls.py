"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# myproject/urls.py



from django.conf import settings
from django.conf.urls.static import static
from inova.views import teste, index, catalogo_startup, perfil_startup, login_view
from inova import views
from django.contrib import admin
from django.urls import path




urlpatterns = [
    path('inbate''admin/', admin.site.urls),
    path('inbate''home_pagina', views.index, name='home'),
    path('inbate/teste/', views.teste, name='teste'),
    path('inbate/catalogo_startup/', views.catalogo_startup, name='catalogo_startup'),
    path('inbate/perfil_startup/<str:nome>/',
         views.perfil_startup, name='perfil_startup'),
    path('inbate/criar_startup/', views.criar_startup, name='criar_startup'),
    path('inbate/perfil_projeto/<str:startup_nome>/<str:projeto_nome>/',
         views.perfil_projeto, name='perfil_projeto'),
    path('inbate/login/', login_view, name='login'),
    path('perfil_startup/<str:nome>/', perfil_startup, name='perfil_startup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urls.py


'''if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])'''