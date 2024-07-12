# forms.py

from django import forms
from .models import Startup


class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = [
            'nome', 'descricao', 'cnpj', 'area_de_negocio', 'setor',
            'email', 'telefone', 'logo_startup', 'rua', 'numero',
            'bairro', 'cidade', 'estado', 'cep', 'pais'
        ]
