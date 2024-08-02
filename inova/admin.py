from django.contrib import admin
from inova.models import Startup, Noticias, Projeto

class ProjetoInline(admin.TabularInline):
    model = Projeto
    extra = 1  # Número de formulários vazios para novos projetos

class Startups_admin(admin.ModelAdmin):
    # List_display mostra os dados na tela do admin
    list_display = (
        'nome', 'cnpj', 'area_de_negocio', 'setor', 'email', 'telefone',
        'logo_startup', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'pais'
    )
    # search_fields são os dados utilizados como filtros para o admin
    search_fields = ('setor', 'nome', 'area_de_negocio', 'cidade', 'estado', 'pais')
    inlines = [ProjetoInline]



class Noticias_admin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'imagem', 'link')
    search_fields = ('nome', 'descricao')

class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'link_video', 'startup')
    search_fields = ('nome', 'descricao', 'startup__nome')


admin.site.register(Noticias, Noticias_admin)
admin.site.register(Startup, Startups_admin)
admin.site.register(Projeto, ProjetoAdmin)
