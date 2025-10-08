
"""
Define as views (lógica de requisição e resposta) para a aplicação 'inova'.

Este módulo contém todas as views da aplicação, que são responsáveis por
processar as requisições HTTP dos usuários e retornar as respostas adequadas.
Inclui uma view baseada em função para a página inicial e views baseadas em
classes (CBVs) para as operações de CRUD (Criar, Ler, Atualizar, Deletar)
do modelo `Noticia`.
"""

from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Startup, MembroEquipe, RedesSociais, Contato
from .forms import StartupForm, ContatoForm, RedesSociaisForm, MembroEquipeFormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Noticia
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import NoticiaForm
from .models import Startup


def pagina_inicial(request):
    
    """
    Renderiza a página inicial da aplicação (home).

    Esta view busca as 9 notícias mais recentes no banco de dados e as
    envia como contexto para o template 'home.html'.

    Args:
        request (HttpRequest): O objeto da requisição HTTP.

    Returns:
        HttpResponse: Uma resposta HTTP contendo a página inicial renderizada.
    """
    
    noticias = Noticia.objects.all().order_by('-data_publicacao')[:9]  
    return render(request, 'home.html', {'noticias': noticias})

class NoticiaListView(ListView):
    
    """
    Exibe uma lista paginada de todas as notícias.

    Esta view herda de `ListView` do Django para listar todas as instâncias do
    modelo `Noticia`, ordenadas pela data de publicação (conforme definido no
    modelo Meta). A lista é paginada para exibir um número fixo de notícias
    por página.

    Atributos:
        model (Model): O modelo a ser listado (`Noticia`).
        template_name (str): O caminho para o template que renderizará a lista.
        context_object_name (str): O nome da variável de contexto no template.
        paginate_by (int): O número de notícias a serem exibidas por página.
    """
    
    model = Noticia
    template_name = 'inova/noticia_list.html'  
    context_object_name = 'noticias'
    paginate_by = 9

class NoticiaDetailView(DetailView):
    
    """
    Exibe os detalhes completos de uma única notícia.

    Esta view herda de `DetailView` para buscar e exibir uma instância
    específica do modelo `Noticia`, identificada pela sua chave primária (PK)
    na URL.
    
    Atributos:
        model (Model): O modelo do qual o detalhe será exibido (`Noticia`).
        template_name (str): O caminho para o template de detalhe.
    """
    
    model = Noticia
    template_name = 'inova/noticia_detail.html'

class NoticiaCreateView(LoginRequiredMixin, CreateView):
    
    """
    View para a criação de uma nova notícia.

    Acesso restrito a usuários logados através do `LoginRequiredMixin`.
    Utiliza o `NoticiaForm` para renderizar e validar os dados do formulário.
    Após a criação bem-sucedida, o usuário é redirecionado para a lista de notícias.

    Atributos:
        model (Model): O modelo a ser criado (`Noticia`).
        form_class (Form): O formulário a ser utilizado (`NoticiaForm`).
        template_name (str): O caminho para o template do formulário.
        success_url (str): A URL para redirecionar após o sucesso.
    """
    
    model = Noticia
    form_class = NoticiaForm
    template_name = 'inova/noticia_form.html'
    success_url = reverse_lazy('noticia_list')

    def form_valid(self, form):
        
        """
        Associa o usuário logado como administrador da notícia.

        Este método é chamado quando os dados do formulário são válidos. Antes de
        salvar, ele atribui o usuário da requisição atual ao campo 'administrador'
        da instância da notícia.

        Args:
            form (ModelForm): A instância do formulário com os dados validados.

        Returns:
            HttpResponseRedirect: Redireciona para a `success_url`.
        """
        
        form.instance.administrador = self.request.user
        return super().form_valid(form)

class NoticiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    """
    View para a atualização de uma notícia existente.

    Protegida por `LoginRequiredMixin` (requer login) e `UserPassesTestMixin`
    (requer que o usuário passe em um teste de permissão). Permite a edição
    de uma notícia apenas pelo seu criador ou por um superusuário.

    Atributos:
        model (Model): O modelo a ser atualizado (`Noticia`).
        form_class (Form): O formulário a ser utilizado (`NoticiaForm`).
        template_name (str): O caminho para o template do formulário.
        success_url (str): A URL para redirecionar após o sucesso.
    """
    
    model = Noticia
    form_class = NoticiaForm
    template_name = 'inova/noticia_form.html'
    success_url = reverse_lazy('noticia_list')

    def test_func(self):
        
        """
        Verifica se o usuário tem permissão para editar a notícia.

        Este método é exigido pelo `UserPassesTestMixin`.

        Returns:
            bool: True se o usuário logado for o administrador da notícia ou
                  um superusuário, False caso contrário.
        """
        
        noticia = self.get_object()
        return noticia.administrador == self.request.user or self.request.user.is_superuser

class NoticiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    """
    View para a exclusão de uma notícia existente.

    Exige que o usuário confirme a exclusão em uma página intermediária.
    O acesso é restrito ao administrador que criou a notícia ou a um
    superusuário, através dos mixins de login e teste de permissão.

    Atributos:
        model (Model): O modelo a ser deletado (`Noticia`).
        template_name (str): O caminho para o template de confirmação.
        success_url (str): A URL para redirecionar após a exclusão.
    """
    
    model = Noticia
    template_name = 'inova/noticia_confirm_delete.html'
    success_url = reverse_lazy('noticia_list')

    def test_func(self):
        
        """
        Verifica se o usuário tem permissão para excluir a notícia.

        Este método é exigido pelo `UserPassesTestMixin`.

        Returns:
            bool: True se o usuário logado for o administrador da notícia ou
                  um superusuário, False caso contrário.
        """
        
        noticia = self.get_object()
        return noticia.administrador == self.request.user or self.request.user.is_superuser
    


def catalogo(request):
    
    
    startups = Startup.objects.all()

    # Estatísticas
    total_startups = startups.count()
    total_setores = startups.values('setor_atuacao').distinct().count()
    total_incubadoras = startups.values('incubadora').distinct().count()

    context = {
        'startups': startups,
        'total_startups': total_startups,
        'total_setores': total_setores,
        'total_incubadoras': total_incubadoras,
    }

    return render(request, 'catalogo.html', context)

def perfil_startup(request, startup_id):


    # Pega a startup pelo ID
    startup = get_object_or_404(Startup, id=startup_id)

    # Pega todos os membros da equipe
    equipe = MembroEquipe.objects.filter(startup=startup)

    # Pega contato e redes sociais, se existirem
    contato = getattr(startup, 'contato', None)
    redes = getattr(startup, 'redes_sociais', None)
    
    context = {
        'startup': startup,
        'equipe': equipe,
        'contato': contato,
        'redes': redes
    }

    return render(request, 'perfil.html', context)
