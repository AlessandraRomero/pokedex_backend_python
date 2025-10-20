from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import TipoPokemon
from core.serializers import TipoPokemonSerializer


class TipoPokemonViewSet(viewsets.ModelViewSet):

    queryset = TipoPokemon.objects.all().order_by("descricao")
    serializer_class = TipoPokemonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        descricao = self.request.query_params.get("descricao")

        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao.lower())

        return queryset
