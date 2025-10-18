

"""
Define os formulários da aplicação baseados nos modelos.

Este módulo contém todas as classes de formulário (`ModelForm`) usadas para
criar, validar e processar dados inseridos pelos usuários. Os formulários
são baseados nos modelos definidos em `models.py` e incluem personalizações
de widgets, labels e validações.

Também define um `inlineformset_factory` para o gerenciamento de múltiplos
membros de equipe associados a uma única Startup.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Startup, MembroEquipe, RedesSociais, Contato
from .models import Noticia

# CSS_CLASS é uma forma de adicionar classes CSS a todos os campos
# para facilitar a estilização com o Bootstrap
CSS_CLASS = 'form-control'

class StartupForm(forms.ModelForm):
    
    """
    Formulário para criar e atualizar os dados principais de uma Startup.
    
    Este `ModelForm` está vinculado ao modelo `Startup` e personaliza a
    renderização de seus campos através da classe Meta, definindo os campos
    exibidos, seus rótulos e os widgets HTML.
    """
    
    class Meta:
        
        """
        Configurações do formulário, associando-o ao modelo Startup.
        
        As informações coletadas para o cadastro das startups são:
        
        nome da startup,
        logo da startup,
        sobre a startup,
        como a UFPI contribui com a startup,
        ano de fundação,
        setor de atuação,
        tamanho da equipe,
        incubadora.
        
        """
        
        model = Startup
        fields = [
            'nome_startup',
            'logo_startup',
            'sobre_a_startup',
            'como_UFPI_contribuiu',
            'ano_fundacao',
            'setor_atuacao',
            'tamanho_equipe',
            'incubadora',
        ]
        
        # Labels personalizados para cada campo
        labels = {
            'nome_startup': 'Nome da Startup',
            'logo_startup': 'Logo da Startup',
            'sobre_a_startup': 'Sobre a Startup',
            'como_UFPI_contribuiu': 'Como a UFPI contribuiu para o projeto?',
            'ano_fundacao': 'Ano de Fundação',
            'setor_atuacao': 'Setor de Atuação',
            'tamanho_equipe': 'Tamanho da Equipe',
            'incubadora': 'Faz parte de alguma incubadora? Qual?',
        }

        # Widgets para customizar o tipo e a aparência dos campos no HTML
        widgets = {
            'nome_startup': forms.TextInput(attrs={'class': CSS_CLASS, 'placeholder': 'Ex: InovaTech'}),
            'logo_startup': forms.FileInput(attrs={'class': CSS_CLASS}),
            'sobre_a_startup': forms.Textarea(attrs={'class': CSS_CLASS, 'rows': 4}),
            'como_UFPI_contribuiu': forms.Textarea(attrs={'class': CSS_CLASS, 'rows': 4}),
            'ano_fundacao': forms.NumberInput(attrs={'class': CSS_CLASS, 'placeholder': 'Ex: 2024'}),
            'setor_atuacao': forms.TextInput(attrs={'class': CSS_CLASS, 'placeholder': 'Ex: Tecnologia, Saúde, Educação'}),
            'tamanho_equipe': forms.TextInput(attrs={'class': CSS_CLASS, 'placeholder': 'Ex: 1-5, 6-10, 11-20'}),
            'incubadora': forms.TextInput(attrs={'class': CSS_CLASS, 'placeholder': 'Ex: Parnaíba Valley'}),
        }


class ContatoForm(forms.ModelForm):
    
    """
    Formulário para os dados de contato associados a uma Startup.

    Vinculado ao modelo `Contato`, este formulário exclui o campo `startup`,
    pois a associação é gerenciada pela view que processa o formulário,
    garantindo que o contato seja ligado à `Startup` correta.
    """
    
    class Meta:
        
        """
        Configurações do ContatoForm.
        
        As informações coletadas para o cadastro do contato são:
        
        email,
        telefone,
        website oficial da startup.
        
        """
        
        model = Contato
        exclude = ['startup'] # O campo 'startup' será associado na view
        labels = {
            'email_startup': 'E-mail de Contato',
            'telefone_startup': 'Telefone (com DDD)',
            'site_startup': 'Website Oficial',
        }
        widgets = {
            'email_startup': forms.EmailInput(attrs={'class': CSS_CLASS, 'placeholder': 'contato@suastartup.com'}),
            'telefone_startup': forms.TextInput(attrs={'class': CSS_CLASS, 'placeholder': '(86) 99999-9999'}),
            'site_startup': forms.URLInput(attrs={'class': CSS_CLASS, 'placeholder': 'https://www.suastartup.com'}),
        }


class RedesSociaisForm(forms.ModelForm):
    
    """Formulário para os links de redes sociais de uma Startup."""
    
    class Meta:
        
        """
        Configurações do RedesSociaisForm.
        
        As informações coletadas para o cadastro das redes sociais são:
        
        link do linkedin,
        link do facebook,
        link do instagram,
        link do twitter.
        
        """
        
        model = RedesSociais
        exclude = ['startup']
        # Usar placeholders já é bastante descritivo aqui
        widgets = {
            'linkedin': forms.URLInput(attrs={'class': CSS_CLASS, 'placeholder': 'URL do LinkedIn'}),
            'facebook': forms.URLInput(attrs={'class': CSS_CLASS, 'placeholder': 'URL do Facebook'}),
            'instagram': forms.URLInput(attrs={'class': CSS_CLASS, 'placeholder': 'URL do Instagram'}),
            'twitter': forms.URLInput(attrs={'class': CSS_CLASS, 'placeholder': 'URL do Twitter (X)'}),
        }


class MembroEquipeForm(forms.ModelForm):
    
    """Formulário para os dados de um único membro da equipe de uma Startup."""
    
    class Meta:
        
        """
        Configurações do MembroEquipeForm.
        
        As informações coletadas para o cadastro de um membro da equipe são:
        
        nome completo,
        cargo/função,
        foto do membro.
        
        """
        
        model = MembroEquipe
        exclude = ['startup']
        labels = {
            'nome_membro': 'Nome Completo',
            'funcao_membro': 'Cargo / Função',
            'foto_membro': 'Foto do Membro (Opcional)',
        }
        widgets = {
            'nome_membro': forms.TextInput(attrs={'class': CSS_CLASS}),
            'funcao_membro': forms.TextInput(attrs={'class': CSS_CLASS, 'placeholder': 'Ex: CEO, Desenvolvedor(a) Backend'}),
            'foto_membro': forms.FileInput(attrs={'class': CSS_CLASS}),
        }


# O InlineFormSet é a forma mais poderosa de gerenciar objetos relacionados.
# Ele criará múltiplos formulários de MembroEquipe ligados a uma única Startup.

MembroEquipeFormSet = inlineformset_factory(
    Startup,           # Modelo Pai
    MembroEquipe,      # Modelo Filho
    form=MembroEquipeForm, # Formulário a ser usado para cada filho
    extra=1,           # Quantos formulários em branco devem ser exibidos por padrão
    can_delete=True,   # Permite que o usuário marque membros para exclusão
    min_num=1,         # Exige que pelo menos um membro seja cadastrado
    validate_min=True, # Garante a validação do min_num
)


class NoticiaForm(forms.ModelForm):
    
    """Formulário para criar e atualizar instâncias do modelo Noticia."""
    
    class Meta:
        
        """
        Configurações do NoticiaForm.
        As informações coletadas para o cadastro das noticias são:
        
        titulo,
        descrição,
        data de publicação,
        categoria.
        
        """
        
        model = Noticia
        fields = ['titulo', 'descricao', 'data_publicacao', 'categoria']
