from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    dt_nascimento = models.DateField(null=True, blank=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    dt_alteracao = models.DateTimeField(auto_now=True)

class TipoPokemon(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao

class PokemonUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_pokemon = models.ForeignKey(TipoPokemon, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20)
    imagem_url = models.URLField()
    nome = models.CharField(max_length=100)
    geracao = models.IntegerField(null=True, blank=True)
    grupo_batalha = models.BooleanField(default=False)
    favorito = models.BooleanField(default=False)
    altura = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    base_experiencia = models.IntegerField(null=True, blank=True)
    especie = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    tipo_secundario = models.CharField(max_length=50, null=True, blank=True)
    habilidades = models.JSONField(null=True, blank=True)
    stats = models.JSONField(null=True, blank=True)
    habitat = models.CharField(max_length=100, null=True, blank=True)