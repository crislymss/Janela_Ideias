from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

class Startup(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.TextField(
        default='descrição...', blank=False, null=False)
    cnpj = models.CharField(max_length=200, blank=False, null=False)
    area_de_negocio = models.CharField(max_length=200, blank=False, null=False)
    setor = models.CharField(max_length=200, blank=False, null=False)
    email = models.CharField(max_length=200, blank=False, null=False)
    telefone = models.CharField(max_length=200, blank=False, null=False)
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



"""class Administrador(AbstractBaseUser):
    startup = models.OneToOneField(Startup, related_name='administrador', on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, blank=False, null=False)
    cargo = models.CharField(max_length=200, blank=False, null=False)
    formacao = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    linkedin = models.URLField(blank=True, null=True)
    senha = models.CharField(max_length=128, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cargo', 'formacao']"""

class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    formacao = models.CharField(max_length=100)
    email = models.EmailField()  # Corrigido
    linkedin = models.URLField()
    foto = models.ImageField(
        upload_to='media/membros/', blank=True, null=True)
    senha = models.CharField(max_length=128)  # Opcional, se necessário

    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='administrador')

    def __str__(self):
        return self.nome

class Membro(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    formacao = models.CharField(max_length=100)
    email = models.EmailField()
    linkedin = models.URLField()
    foto = models.ImageField(
        upload_to='media/membros/', blank=True, null=True)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='membros')

    def __str__(self):
        return self.nome




class Projeto(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.TextField(blank=False, null=False)
    link_video = models.URLField(blank=True, null=True)
    startup = models.ForeignKey(Startup, related_name='projetos', on_delete=models.CASCADE)
    logo_projeto = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto1 = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto2 = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto3 = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto4 = models.ImageField(upload_to='inova/', blank=True, null=True)
    foto5 = models.ImageField(upload_to='inova/', blank=True, null=True)
    coordenador = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, blank=True, related_name='projetos_coordenados')

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        fotos = [self.foto1, self.foto2, self.foto3, self.foto4, self.foto5]
        fotos_preenchidas = [foto for foto in fotos if foto]
        if not (2 <= len(fotos_preenchidas) <= 5):
            raise ValidationError('O projeto deve ter entre 2 e 5 fotos.')

    def save(self, *args, **kwargs):
        # Certifique-se de que a startup já foi salva antes de tentar definir o coordenador
        if not self.startup.administrador:
            raise ValidationError("A startup não possui um administrador.")

        self.coordenador = self.startup.administrador

        # Chame o método save padrão
        super().save(*args, **kwargs)

class MembroProjeto(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='membros')

