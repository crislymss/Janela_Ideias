
"""
Define os modelos de banco de dados para a aplicação 'inova'.

Este módulo contém todas as classes de modelo do Django que estruturam os dados
da aplicação. O modelo principal é `Startup`, que se relaciona com `MembroEquipe`,
`RedesSociais` e `Contato`. O modelo `Noticia` gerencia o conteúdo de notícias
do sistema.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone

class Startup(models.Model):
    
    """
    Representa uma startup cadastrada no sistema.

    Este é o modelo central que armazena as informações principais de uma startup,
    incluindo seu nome, descrição, ano de fundação e outros dados relevantes.
    
    Atributos:
        nome_startup (CharField): O nome oficial da startup.
        sobre_a_startup (TextField): Uma descrição detalhada sobre a startup.
        como_UFPI_contribuiu (TextField): Descrição de como a UFPI apoiou o projeto.
        ano_fundacao (IntegerField): O ano em que a startup foi fundada.
        setor_atuacao (CharField): O principal setor de mercado em que a startup atua.
        tamanho_equipe (CharField): Faixa que representa o número de membros na equipe.
        incubadora (CharField): Nome da incubadora à qual a startup possa pertencer.
        logo_startup (ImageField): Arquivo de imagem com o logo da startup.
    """
    
    nome_startup = models.CharField(max_length=100)
    sobre_a_startup = models.TextField()
    como_UFPI_contribuiu = models.TextField(verbose_name="Como a UFPI contribuiu?", null=True, blank=True)
    ano_fundacao = models.IntegerField(default=0, verbose_name="Ano de Fundação")
    setor_atuacao = models.CharField(max_length=100, verbose_name="Setor de Atuação")
    tamanho_equipe = models.CharField(default=0, verbose_name="Tamanho da Equipe")
    incubadora = models.CharField(max_length=100, blank=True) 
    logo_startup = models.ImageField(upload_to='logos_startups/', blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Criação")
    
    administrador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Se o usuário for deletado, o campo fica nulo
        null=True,
        blank=True,
        related_name='startups_criadas', # Use um related_name único
        verbose_name="Administrador"
    )
    
    def __str__(self):
        
        """Retorna o nome da startup como sua representação em string."""
        
        return self.nome_startup


class MembroEquipe(models.Model):
    
    """
    Representa um membro da equipe de uma startup.

    Cada instância deste modelo está ligada a uma `Startup` através de uma
    chave estrangeira (relação muitos-para-um).
    
    Atributos:
        startup (ForeignKey): A referência à Startup à qual o membro pertence.
        nome_membro (CharField): O nome completo do membro da equipe.
        funcao_membro (CharField): O cargo ou função do membro na startup.
        foto_membro (ImageField): Foto do membro da equipe.
    """
    
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='membros')
    
    nome_membro = models.CharField(max_length=100, verbose_name="Nome do Membro")
    funcao_membro = models.CharField(max_length=100, verbose_name="Função")
    foto_membro = models.ImageField(upload_to='fotos_membros/', blank=True, null=True)

    def __str__(self):
        
        """Retorna o nome do membro e o nome da startup associada."""
        
        return f"{self.nome_membro} ({self.startup.nome_startup})"


class RedesSociais(models.Model):
    
    """
    Armazena os links das redes sociais de uma startup.

    Utiliza uma relação um-para-um com o modelo `Startup`, garantindo que
    cada startup tenha apenas um conjunto de links de redes sociais.
    
    Atributos:
        startup (OneToOneField): A referência à Startup associada.
        linkedin (URLField): URL para o perfil do LinkedIn.
        facebook (URLField): URL para o perfil do Facebook.
        instagram (URLField): URL para o perfil do Instagram.
        twitter (URLField): URL para o perfil do Twitter (X).
    """
    
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='redes_sociais')
    
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        
        """Retorna uma string identificando as redes sociais da startup."""
        
        return f"Redes Sociais da {self.startup.nome_startup}"


class Contato(models.Model):
    
    """
    Armazena as informações de contato de uma startup.

    Utiliza uma relação um-para-um com o modelo `Startup`, garantindo que
    cada startup tenha apenas um conjunto de informações de contato.
    
    Atributos:
        startup (OneToOneField): A referência à Startup associada.
        email_startup (EmailField): Endereço de e-mail principal da startup.
        telefone_startup (CharField): Número de telefone para contato.
        site_startup (URLField): URL do website oficial da startup.
    """
    
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='contato')
    
    email_startup = models.EmailField(verbose_name="E-mail")
    telefone_startup = models.CharField(max_length=20, verbose_name="Telefone") 
    site_startup = models.URLField(blank=True, null=True, verbose_name="Site")

    def __str__(self):
        
        """Retorna uma string identificando o contato da startup."""
        
        return f"Contato da {self.startup.nome_startup}"
    


class Noticia(models.Model):
    
    """
    Representa um artigo de notícia publicado no sistema.
    
    Este modelo armazena todo o conteúdo de uma notícia, incluindo título,
    descrição, categoria e o administrador que a publicou.
    
    Atributos:
        id_noticia (AutoField): Chave primária autoincrementável.
        titulo (CharField): O título da notícia.
        descricao (TextField): O conteúdo completo da notícia.
        data_publicacao (DateField): A data em que a notícia foi publicada.
        imagem (ImageField): Imagem de capa para a notícia.
        categoria (CharField): Categoria da notícia, com opções pré-definidas.
        administrador (ForeignKey): Referência ao usuário (admin) que criou a notícia.
            Se o usuário for deletado, este campo se tornará nulo.
        link (URLField): Um link externo relacionado à notícia, se houver.
    """
    
    id_noticia = models.AutoField(primary_key=True)
    titulo = models.CharField("Título", max_length=255)
    descricao = models.TextField("Descrição")
    data_publicacao = models.DateField("Data de publicação", default=timezone.now)
    imagem = models.ImageField(upload_to='noticias/', blank=True, null=True)
    
    CATEGORIA_CHOICES = [
        ('STARTUP', 'Startups'),
        ('INOVACAO', 'Inovação'),
        ('EVENTO', 'Eventos'),
        ('PESQUISA', 'Pesquisa'),
        ('TECNOLOGIA', 'Tecnologia'),
        ('INSTITUCIONAL', 'Institucional'),
        ('OUTROS', 'Outros'),
    ]
    
    categoria = models.CharField("Categoria", max_length=20, choices=CATEGORIA_CHOICES)
    
    
    administrador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  
        null=True,
        blank=True,
        related_name='noticias'
    )

    link = models.URLField("Link da notícia", max_length=500, blank=True, null=True)

    class Meta:
        
        """Define metadados para o modelo Noticia."""
        
        ordering = ['-data_publicacao']
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'

    def __str__(self):
        
        """Retorna o título da notícia como sua representação em string."""
        
        return self.titulo


class LinkFormulario(models.Model):
    
    """
    Representa um link de formulário que pode ser atualizado pelos administradores.
    
    Este modelo permite que os administradores mantenham e atualizem links de
    formulários importantes, com controle de data de atualização.
    
    Atributos:
        link (URLField): URL do formulário.
        data (DateTimeField): Data e hora da última atualização do link.
    """
    
    link = models.URLField("Link do Formulário", max_length=500)
    data = models.DateTimeField("Data de Atualização", auto_now=True)
    
    administrador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='links_cadastrados', # Use um related_name único
        verbose_name="Administrador"
    )
    
    class Meta:
        
        """Define metadados para o modelo LinkFormulario."""
        
        verbose_name = 'Link do Formulário'
        verbose_name_plural = 'Link do Formulário'
        ordering = ['-data']

    def __str__(self):
        
        """Retorna uma representação em string do link do formulário."""
        
        return f"Link do Formulário - {self.data.strftime('%d/%m/%Y %H:%M')}"
    
    