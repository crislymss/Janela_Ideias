from django.contrib import admin
from .models import Startup, Administrador, Membro, Projeto, Noticias, MembroProjeto
from django import forms


class ProjetoInline(admin.TabularInline):
    model = Projeto
    extra = 1

class AdministradorInline(admin.StackedInline):
    model = Administrador
    can_delete = False
    verbose_name_plural = 'Administrador'

class MembroInline(admin.TabularInline):
    model = Membro
    extra = 1

class Startups_admin(admin.ModelAdmin):
    list_display = (
        'nome', 'cnpj', 'area_de_negocio', 'setor', 'email', 'telefone',
        'logo_startup', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'pais'
    )
    search_fields = ('setor', 'nome', 'area_de_negocio', 'cidade', 'estado', 'pais')
    inlines = [ProjetoInline, AdministradorInline, MembroInline]

class Noticias_admin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data', 'imagem', 'link')
    search_fields = ('nome', 'descricao', 'data')

class MembroProjetoInline(admin.TabularInline):
    model = MembroProjeto
    extra = 1


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProjetoForm, self).__init__(*args, **kwargs)
        if 'startup' in self.data:
            try:
                startup_id = int(self.data.get('startup'))
                self.fields['coordenador'].queryset = Administrador.objects.filter(startup=startup_id)
                self.fields['membros'].queryset = Membro.objects.filter(startup=startup_id)
            except (ValueError, TypeError):
                pass  # caso id da startup não seja válido
        elif self.instance.pk:
            self.fields['coordenador'].queryset = Administrador.objects.filter(startup=self.instance.startup)
            self.fields['membros'].queryset = Membro.objects.filter(startup=self.instance.startup)


class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'link_video', 'startup', 'logo_projeto')
    search_fields = ('nome', 'descricao', 'startup__nome')
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'link_video', 'startup', 'logo_projeto', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5')
        }),
    )
    inlines = [MembroProjetoInline]

    def save_model(self, request, obj, form, change):
        obj.coordenador = obj.startup.administrador
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('coordenador',)
        return self.readonly_fields






    
# Aqui são os objetos que aparecem no menu do adm
# 1 Noticias manipula as noticias que aparecem na tela inicial

admin.site.register(Noticias, Noticias_admin)

# 2 Startup_admin faz a gestão das startups

admin.site.register(Startup, Startups_admin)

# 3 Projeto vai gerir os projetos cadastrados na plataforma
admin.site.register(Projeto, ProjetoAdmin)

# 4 Vai gerir os administradores, lembrando que cada startup tem 1(um) administrador
admin.site.register(Administrador)

# 5 Membro faz a gestão dos membros cadastrados, podendo adicionar e vincular a uma startup
# eu removi do menu de administração para evitar poluição desnessesária da tela
# Já que esses membros podem ser adicionados diretamente nas opções da startup
#admin.site.register(Membro)


