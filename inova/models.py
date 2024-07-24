
import os
# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


#mudar o startup para Startup / fazer os migrations
# models.py

class Startup(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.TextField(
        default='descrição...', blank=False, null=False)
    cnpj = models.IntegerField()
    area_de_negocio = models.CharField(max_length=200, blank=False, null=False)
    setor = models.CharField(max_length=200, blank=False, null=False)
    email = models.CharField(max_length=200, blank=False, null=False)
    telefone = models.IntegerField()
    logo_startup = models.ImageField(upload_to='inova/', blank=True, null=True)

    # Novos campos de contato
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True,
                              null=True)  # Use siglas de estados
    cep = models.CharField(max_length=10, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome


class Noticias(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False,null = False)
    descricao = models.TextField(default = 'Descricao')
    imagem = models.ImageField(upload_to = 'media/noticias/', blank = True, null = True)
    link = models.URLField(blank = True, null = True)

    def __str__(self):
        return self.nome
@receiver(post_save, sender=Noticias)
def limitar_quantidade_noticias(sender, instance, **kwargs):
    # Essa parte vai contar as noticias do banco de dados, limitando a 4 noticias

    if Noticias.objects.count() > 4:
        #e vai pegar a notícia mais antiga (a primeira que foi cadastrada)
        noticia_antiga = Noticias.objects.order_by('id').first()

        """
        # Move a imagem da notícia mais antiga para uma pasta diferente
        # Como isso consumiria mais espaço em disco, está em hold, caso 
        # existe a nescessidade de implementar no futuro ja esta encaminhada.
        
        if noticia_antiga.imagem:
            nome_arquivo = os.path.basename(noticia_antiga.imagem.name)
            pasta_antiga = os.path.dirname(noticia_antiga.imagem.name)
            nova_pasta = os.path.join(pasta_antiga, 'noticias_antigas')
            os.makedirs(nova_pasta, exist_ok=True)
            novo_caminho = os.path.join(nova_pasta, nome_arquivo)
            os.rename(noticia_antiga.imagem.path, novo_caminho)"""

        # apaga a noticia antiga
        noticia_antiga.delete()


class Projeto(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.TextField(blank=False, null=False)
    link_video = models.URLField(blank=True, null=True)
    startup = models.ForeignKey(Startup, related_name='projetos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome