from rest_framework import serializers
from .models import TipoPokemon, PokemonUsuario, Usuario

class TipoPokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPokemon
        fields = '__all__'

class PokemonUsuarioSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(source='tipo_pokemon.descricao')
    imagem = serializers.URLField(source='imagem_url')

    class Meta:
        model = PokemonUsuario
        fields = [
            'id',
            'codigo',
            'nome',
            'imagem',
            'tipo',
            'tipo_secundario',
            'favorito',
            'grupo_batalha',
            'geracao',
            'altura',
            'peso',
            'base_experiencia',
            'especie',
            'descricao',
            'habilidades',
            'stats',
            'habitat'
        ]

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'nome']