
"""
Configura a interface de administração do Django para os modelos da aplicação.
Este arquivo registra os modelos da aplicação na área de administração do Django
e personaliza como eles são exibidos e editados. Inclui configurações para
os modelos `Startup` e `Noticia`, utilizando classes `ModelAdmin` customizadas
e inlines para facilitar o gerenciamento de modelos relacionados.
"""


from django.contrib import admin
from .models import Startup, MembroEquipe, RedesSociais, Contato
from .models import Noticia, LinkFormulario

from django.contrib.admin import AdminSite
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.db.models.functions import TruncMonth
from inova.models import LinkFormulario

class CustomAdminSite(AdminSite):
    site_header = "Janela de Ideias"

    def each_context(self, request):
        context = super().each_context(request)

        # Busca o link mais recente cadastrado
        ultimo_link = LinkFormulario.objects.first()

        context["link_formulario"] = ultimo_link.link if ultimo_link else None
        return context


# Crie classes inline para os modelos relacionados ao Startup
# StackedInline mostra os campos um abaixo do outro
class ContatoInline(admin.StackedInline):
    
    """
    Permite a edição de contatos diretamente na página de uma Startup.
    Utiliza um layout empilhado (StackedInline) para exibir os campos de contato.
    """
    
    model = Contato
    extra = 1 # Mostra 1 formulário de contato extra para preenchimento

class RedesSociaisInline(admin.StackedInline):
    
    """
    Permite a edição de redes sociais diretamente na página de uma Startup.
    Utiliza um layout empilhado (StackedInline) para os campos de redes sociais.
    """

    model = RedesSociais
    extra = 1 # Mostra 1 formulário de redes sociais extra

# TabularInline é mais compacto, bom para quando há vários itens
class MembroEquipeInline(admin.TabularInline):
    
    """
    Permite a edição de membros da equipe diretamente na página de uma Startup.
    Utiliza um layout tabular (TabularInline), mais compacto, ideal para listas
    de membros.
    """
    
    model = MembroEquipe
    extra = 1 # Mostra 1 formulário de membro extra

# Crie a classe de administração principal para o modelo Startup
class StartupAdmin(admin.ModelAdmin):
    
    """
    Define a configuração da administração para o modelo Startup.

    Atributos:
        list_display (tuple): Campos a serem exibidos na lista de startups.
        inlines (list): Classes inline para permitir a edição de modelos
            relacionados (Contato, RedesSociais, MembroEquipe) na mesma página.
    """
    
    # Lista de campos que aparecem na listagem de todas as startups
    list_display = ('nome_startup', 'setor_atuacao', 'ano_fundacao', 'logo_startup')
    
    # Adicione os inlines à página de edição da Startup
    inlines = [
        ContatoInline,
        RedesSociaisInline,
        MembroEquipeInline,
    ]

# Registre o modelo Startup usando a classe de admin personalizada
admin.site.register(Startup, StartupAdmin)

# Você pode registrar os outros modelos se quiser acessá-los individualmente também,
# mas não é necessário se você só for editá-los através da página da Startup.
# admin.site.register(MembroEquipe)
# admin.site.register(RedesSociais)
# admin.site.register(Contato)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    
    """
    Define a configuração da administração para o modelo Noticia.

    Atributos:
        list_display (tuple): Campos exibidos na lista de notícias.
        list_filter (tuple): Campos que podem ser usados para filtrar a lista.
        search_fields (tuple): Campos nos quais a busca será realizada.
        date_hierarchy (str): Adiciona uma navegação hierárquica por data.
    """
    
    list_display = ('titulo', 'categoria', 'data_publicacao', 'administrador', 'link')
    list_filter = ('categoria', 'data_publicacao')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_publicacao'


@admin.register(LinkFormulario)
class LinkFormularioAdmin(admin.ModelAdmin):
    
    """
    Define a configuração da administração para o modelo LinkFormulario.

    Atributos:
        list_display (tuple): Campos exibidos na lista de links de formulários.
        search_fields (tuple): Campos nos quais a busca será realizada.
        date_hierarchy (str): Adiciona uma navegação hierárquica por data.
        readonly_fields (tuple): Campos que não podem ser editados.
    """
    
    list_display = ('link', 'data')
    search_fields = ('link',)
    date_hierarchy = 'data'
    readonly_fields = ('data',)
    
    fieldsets = (
        (None, {
            'fields': ('link',)
        }),
    )

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        # Total de Startups
        total_startups = Startup.objects.count()
        
        # Recentes (Últimos 7 dias)
        recentes_count = Startup.objects.filter(
            data_criacao__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()

        # Últimas Startups
        ultimas_startups = Startup.objects.order_by('-data_criacao')[:3]
        
        # Gráfico: Startups por Mês
        chart_data = [0] * 12
        startups_por_mes = Startup.objects.annotate(
            mes=TruncMonth('data_criacao')
        ).values('mes').annotate(
            total=Count('id')
        ).order_by('mes')

        for item in startups_por_mes:
            if item['mes'] and 1 <= item['mes'].month <= 12:
                chart_data[item['mes'].month - 1] = item['total']
        
        chart_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

        # Última atualização do formulário 
        ultimo_link = LinkFormulario.objects.first()
        data_formulario = ultimo_link.data if ultimo_link else None

        # Adiciona tudo ao contexto
        extra_context = extra_context or {}
        extra_context['total_startups'] = total_startups
        extra_context['recentes_count'] = recentes_count
        extra_context['ultimas_startups'] = ultimas_startups
        extra_context['chart_labels'] = chart_labels
        extra_context['chart_data'] = chart_data
        extra_context['data_formulario'] = data_formulario  # adiciona a data
        
        return super().index(request, extra_context)


# --- 3. REGISTRO NO NOVO 'admin_site' ---

admin_site = CustomAdminSite(name='myadmin')

admin_site.register(Startup, StartupAdmin)
admin_site.register(Noticia, NoticiaAdmin)
admin_site.register(LinkFormulario, LinkFormularioAdmin)
admin_site.register(User)
admin_site.register(Group)

