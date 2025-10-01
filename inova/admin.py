from django.contrib import admin
from .models import Startup, MembroEquipe, RedesSociais, Contato
from .models import Noticia

# Crie classes inline para os modelos relacionados ao Startup
# StackedInline mostra os campos um abaixo do outro
class ContatoInline(admin.StackedInline):
    model = Contato
    extra = 1 # Mostra 1 formulário de contato extra para preenchimento

class RedesSociaisInline(admin.StackedInline):
    model = RedesSociais
    extra = 1 # Mostra 1 formulário de redes sociais extra

# TabularInline é mais compacto, bom para quando há vários itens
class MembroEquipeInline(admin.TabularInline):
    model = MembroEquipe
    extra = 1 # Mostra 1 formulário de membro extra

# Crie a classe de administração principal para o modelo Startup
class StartupAdmin(admin.ModelAdmin):
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
    list_display = ('titulo', 'categoria', 'data_publicacao', 'administrador', 'link')
    list_filter = ('categoria', 'data_publicacao')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_publicacao'
