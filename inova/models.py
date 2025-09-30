from django.db import models

class Startup(models.Model):
    nome_startup = models.CharField(max_length=100)
    sobre_a_startup = models.TextField()
    como_UFPI_contribuiu = models.TextField(verbose_name="Como a UFPI contribuiu?", null=True, blank=True)
    ano_fundacao = models.IntegerField(default=0, verbose_name="Ano de Fundação")
    setor_atuacao = models.CharField(max_length=100, verbose_name="Setor de Atuação")
    tamanho_equipe = models.CharField(max_length=100, verbose_name="Tamanho da Equipe")
    incubadora = models.CharField(max_length=100, blank=True) 
    logo_startup = models.ImageField(upload_to='logos_startups/', blank=True, null=True)

    def __str__(self):
        return self.nome_startup


class MembroEquipe(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='membros')
    
    nome_membro = models.CharField(max_length=100, verbose_name="Nome do Membro")
    funcao_membro = models.CharField(max_length=100, verbose_name="Função")
    foto_membro = models.ImageField(upload_to='fotos_membros/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome_membro} ({self.startup.nome_startup})"


class RedesSociais(models.Model):
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='redes_sociais')
    
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Redes Sociais da {self.startup.nome_startup}"


class Contato(models.Model):
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='contato')
    
    email_startup = models.EmailField(verbose_name="E-mail")
    telefone_startup = models.CharField(max_length=20, verbose_name="Telefone") 
    site_startup = models.URLField(blank=True, null=True, verbose_name="Site")

    def __str__(self):
        return f"Contato da {self.startup.nome_startup}"