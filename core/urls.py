from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views.pokeapi import consultar_pokeapi, importar_pokemon
from core.views.pokemons import PokemonUsuarioViewSet, listar_favoritos
from core.views.tipos import TipoPokemonViewSet

router = DefaultRouter()
router.register(r'tipos', TipoPokemonViewSet)
router.register(r'pokemons', PokemonUsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('pokemons/consultar/<str:nome>/', consultar_pokeapi),

    path('pokemons/importar/<str:nome>/', importar_pokemon()),

    path('favoritos/', listar_favoritos, name='listar_favoritos'),

]