from .models import Startup, Projeto  # Certifique-se de ter esses modelos definidos
from django.shortcuts import render, get_object_or_404
from .models import Startup, Noticias
from django.shortcuts import render, get_object_or_404
from .models import Startup, Projeto


# views.py


from django.shortcuts import render, redirect
from .forms import StartupForm


def criar_startup(request):
    if request.method == 'POST':
        form = StartupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StartupForm()
    return render(request, 'criar_startup.html', {'form': form})


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
    return render(request, 'perfil_startup.html', {'startup': startup, 'projetos': projetos})


def perfil_projeto(request, startup_nome, projeto_nome):
    startup = get_object_or_404(Startup, nome=startup_nome)
    projeto = get_object_or_404(Projeto, startup=startup, nome=projeto_nome)
    return render(request, 'perfil_projeto.html', {'startup': startup, 'projeto': projeto})
