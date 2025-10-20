from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from core.models import PokemonUsuario
from core.serializers import PokemonUsuarioSerializer

class PokemonUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = PokemonUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        queryset = PokemonUsuario.objects.filter(usuario=usuario)
        if self.request.query_params.get("geracao"):
            queryset = queryset.filter(geracao=self.request.query_params["geracao"])
        if self.request.query_params.get("grupo_batalha") == "true":
            queryset = queryset.filter(grupo_batalha=True)
        return queryset

    @action(detail=True, methods=["post"])
    def favoritar(self, request, pk=None):
        pokemon = self.get_object()
        pokemon.favorito = not pokemon.favorito
        pokemon.save()
        estado = "favoritado" if pokemon.favorito else "removido dos favoritos"
        return Response({"detail": f"Pokémon {estado} com sucesso."})

    @action(detail=True, methods=["post"])
    def adicionar_a_equipe(self, request, pk=None):
        usuario = request.user
        if PokemonUsuario.objects.filter(usuario=usuario, grupo_batalha=True).count() >= 6:
            raise ValidationError("Você só pode ter até 6 Pokémon na equipe.")
        pokemon = self.get_object()
        pokemon.grupo_batalha = True
        pokemon.save()
        return Response({"detail": f"{pokemon.nome.title()} adicionado à equipe."})

    @action(detail=True, methods=["post"])
    def remover_da_equipe(self, request, pk=None):
        pokemon = self.get_object()
        if not pokemon.grupo_batalha:
            return Response({"detail": "Este Pokémon já não está na equipe."}, status=400)
        pokemon.grupo_batalha = False
        pokemon.save()
        return Response({"detail": "Pokémon removido da equipe."})

# 🔹 fora da classe!
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_favoritos(request):
    """Lista todos os Pokémon favoritados do usuário autenticado."""
    favoritos = PokemonUsuario.objects.filter(usuario=request.user, favorito=True)
    serializer = PokemonUsuarioSerializer(favoritos, many=True)
    return Response(serializer.data)