
"""
Configura a interface de administração do Django para os modelos da aplicação.
Este arquivo registra os modelos da aplicação na área de administração do Django
e personaliza como eles são exibidos e editados. Inclui configurações para
os modelos `Startup` e `Noticia`, utilizando classes `ModelAdmin` customizadas
e inlines para facilitar o gerenciamento de modelos relacionados.
"""


from django.contrib import admin
from .models import Startup, MembroEquipe, RedesSociais, Contato
from .models import Noticia

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
    list_display = ('nome_startup', 'setor_atuacao', 'ano_fundacao')
    
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
