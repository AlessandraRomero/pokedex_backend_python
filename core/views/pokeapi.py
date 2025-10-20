from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import TipoPokemon, PokemonUsuario
from core.serializers import PokemonUsuarioSerializer
from core.services.pokeapi import buscar_pokemon_da_pokeapi, buscar_geracao_do_pokemon
from core.services.traducao import traduzir_texto
from core.services.importacao import importar_pokemon


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def importar_pokemon_view(request, nome):

    pokemon, erro = importar_pokemon(request.user, nome)

    if erro:
        return Response({'detail': erro}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PokemonUsuarioSerializer(pokemon)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def consultar_pokeapi(request, nome):
    dados = buscar_pokemon_da_pokeapi(nome)
    return Response(dados or {"detail": "Pokémon não encontrado"}, status=200 if dados else 404)
