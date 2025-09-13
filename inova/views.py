from .models import Startup, Projeto
from django.shortcuts import render, get_object_or_404
from .models import Startup, Noticias
from django.shortcuts import render, get_object_or_404
from .models import Startup, Projeto
from django.shortcuts import render, redirect, get_object_or_404
from .models import Startup, Membro, Administrador
from .forms import MembroForm, AdministradorForm, CustomAuthenticationForm
from django.shortcuts import render, redirect
from .forms import StartupForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from functools import wraps

# views.py
# Criar Objetos
