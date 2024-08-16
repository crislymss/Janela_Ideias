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






#Criar Objetos
def criar_startup(request):
    if request.method == 'POST':
        form = StartupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StartupForm()
    return render(request, 'criar_startup.html', {'form': form})

def criar_membro(request):
    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MembroForm()
    return render(request, 'criar_membro.html', {'form': form})

def criar_administrador(request):
    if request.method == 'POST':
        form = AdministradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AdministradorForm()
    return render(request, 'criar_administrador.html', {'form': form})


#Outros
def perfil_startup(request, nome):
    startup = get_object_or_404(Startup, nome=nome)
    projetos = Projeto.objects.filter(startup=startup)
    membros = startup.membros.all()
    administrador = startup.administrador
    return render(request, 'perfil_startup.html', {
        'startup': startup,
        'projetos': projetos,
        'membros': membros,
        'administrador': administrador
    })


def teste(request):
    # PEGA TODOS OS DADOS ->
    # startups = Startup.objects.all()

    # PEGA COM O FILTRO DE SETOR COM PARAMETRO 'TECNOLOGIA' ->
    startups = Startup.objects.filter(setor='tecnologia')

    return render(
        request,
        'teste.html',
        {'startups': startups}
    )


def index(request):
    noticias = Noticias.objects.all()
    return render(
        request,
        'home_pagina.html',
        {'noticias': noticias}
    )


def catalogo_startup(request):
    setor_filter = request.GET.get('setor', '')
    area_negocio_filter = request.GET.get('area_negocio', '')
    search_query = request.GET.get('search', '')

    startups = Startup.objects.all()

    if setor_filter and area_negocio_filter:
        startups = startups.filter(setor=setor_filter) | startups.filter(
            area_de_negocio=area_negocio_filter)
    elif setor_filter:
        startups = startups.filter(setor=setor_filter)
    elif area_negocio_filter:
        startups = startups.filter(area_de_negocio=area_negocio_filter)

    if search_query:
        startups = startups.filter(nome__icontains=search_query)

    setores = Startup.objects.values_list('setor', flat=True).distinct()
    areas_negocio = Startup.objects.values_list(
        'area_de_negocio', flat=True).distinct()

    context = {
        'startups': startups,
        'setores': setores,
        'areas_negocio': areas_negocio,
        'setor_selecionado': setor_filter,
        'area_negocio_selecionada': area_negocio_filter,
        'search_query': search_query,
    }

    return render(request, 'catalogo_startup.html', context)


def perfil_startup(request, nome):
    startup = get_object_or_404(Startup, nome=nome)
    projetos = Projeto.objects.filter(startup=startup)
    membros = Membro.objects.filter(startup=startup)

    # Verifique se há um administrador associado a esta startup
    try:
        administrador = Administrador.objects.get(startup=startup)
    except Administrador.DoesNotExist:
        administrador = None

    context = {
        'startup': startup,
        'projetos': projetos,
        'membros': membros,
        'administrador': administrador
    }

    return render(request, 'perfil_startup.html', context)



def perfil_projeto(request, startup_nome, projeto_nome):
    startup = get_object_or_404(Startup, nome=startup_nome)
    projeto = get_object_or_404(Projeto, startup=startup, nome=projeto_nome)
    membros = projeto.membros.all()  # Assumindo que 'membros' é o related_name usado
    context = {
        'startup': startup,
        'projeto': projeto,
        'membros': membros,
    }
    return render(request, 'perfil_projeto.html', context)




def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            administrador = user.administrador
            return redirect(reverse('perfil_startup', kwargs={'nome': administrador.startup.nome}))
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not hasattr(request.user, 'administrador'):
            raise PermissionDenied

        administrador = request.user.administrador
        startup_nome = kwargs.get('nome')

        if administrador.startup.nome != startup_nome:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return _wrapped_view