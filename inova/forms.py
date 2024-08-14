from django import forms
from .models import Startup, Membro, Administrador
from django import forms
from django.contrib.auth.forms import AuthenticationForm



class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = [
            'nome', 'descricao', 'cnpj', 'area_de_negocio', 'setor',
            'email', 'telefone', 'logo_startup', 'rua', 'numero',
            'bairro', 'cidade', 'estado', 'cep', 'pais'
        ]

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['startup', 'nome', 'cargo', 'formacao', 'email', 'linkedin']

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['startup', 'nome', 'cargo', 'formacao', 'email', 'linkedin', 'senha']



class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not hasattr(user, 'administrador'):
            raise forms.ValidationError(
                "Este usuário não tem acesso a nenhuma startup.",
                code='no_startup'
            )