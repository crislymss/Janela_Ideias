from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome


class Noticias(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.TextField(default='Descricao')
    imagem = models.ImageField(
        upload_to='media/noticias/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    data = models.DateField()

    def __str__(self):
        return self.nome


@receiver(post_save, sender=Noticias)
def limitar_quantidade_noticias(sender, instance, **kwargs):
    if Noticias.objects.count() > 6:
        noticia_antiga = Noticias.objects.order_by('id').first()
        noticia_antiga.delete()


class Projeto(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.TextField(blank=False, null=False)
    link_video = models.URLField(blank=True, null=True)
    startup = models.ForeignKey(
        Startup, related_name='projetos', on_delete=models.CASCADE)
    logo_projeto = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto1 = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto2 = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto3 = models.ImageField(upload_to='inova/', blank=True, null=True)

    def __str__(self):
        return self.nome
