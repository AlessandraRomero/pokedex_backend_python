import requests
from django.core.cache import cache
from .pokeapi import buscar_pokemon_da_pokeapi, buscar_geracao_do_pokemon
from .traducao import traduzir_texto
from ..models import PokemonUsuario, TipoPokemon

CACHE_TTL = 60 * 60 * 24  # 1 dia


def importar_pokemon(usuario, nome):
    nome = nome.lower().strip()

    # 🔹 Cache da PokéAPI
    cache_key_poke = f"pokeapi_{nome}"
    dados = cache.get(cache_key_poke)
    if not dados:
        dados = buscar_pokemon_da_pokeapi(nome)
        if not dados:
            return None, "Pokémon não encontrado."
        cache.set(cache_key_poke, dados, CACHE_TTL)

    # 🔹 Verifica duplicidade
    if PokemonUsuario.objects.filter(usuario=usuario, nome__iexact=nome).exists():
        return None, "Este Pokémon já foi importado."

    # 🔹 Dados básicos
    geracao = buscar_geracao_do_pokemon(nome)
    tipo_nome = dados["types"][0]["type"]["name"]
    tipo_obj, _ = TipoPokemon.objects.get_or_create(descricao=tipo_nome)
    tipo_secundario = dados["types"][1]["type"]["name"] if len(dados["types"]) > 1 else None

    habilidades = [_traduzir_cacheado(h["ability"]["name"]) for h in dados["abilities"]]
    stats = {_traduzir_cacheado(s["stat"]["name"]): s["base_stat"] for s in dados["stats"]}

    altura = round(dados["height"] / 10.0, 1)
    peso = round(dados["weight"] / 10.0, 1)

    # 🔹 Detalhes de espécie (cacheados)
    especie, descricao, habitat = _obter_detalhes_especie_cacheado(dados)

    # 🔹 Criação do Pokémon
    pokemon = PokemonUsuario.objects.create(
        usuario=usuario,
        codigo=dados["id"],
        nome=dados["name"],
        imagem_url=dados["sprites"]["front_default"],
        tipo_pokemon=tipo_obj,
        tipo_secundario=tipo_secundario,
        geracao=geracao,
        habilidades=habilidades,
        stats=stats,
        especie=especie,
        descricao=descricao,
        habitat=habitat,
        altura=altura,
        peso=peso,
        favorito=False,
        grupo_batalha=False,
    )

    return pokemon, None


def _obter_detalhes_especie_cacheado(dados):
    """Obtém detalhes de espécie com cache de 24h."""
    url = dados.get("species", {}).get("url")
    if not url:
        return None, None, None

    cache_key = f"species_{dados['name']}"
    if cached := cache.get(cache_key):
        return cached

    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return None, None, None

        data = resp.json()

        especie = _traduzir_cacheado(data.get("genera", [{}])[0].get("genus", ""))
        habitat = _traduzir_cacheado(data.get("habitat", {}).get("name", ""))

        descricao = next(
            (x["flavor_text"] for x in data["flavor_text_entries"] if x["language"]["name"] == "en"),
            ""
        )
        descricao = _traduzir_cacheado(descricao.replace("\n", " ").replace("\f", " "))

        cache.set(cache_key, (especie, descricao, habitat), CACHE_TTL)
        return especie, descricao, habitat

    except Exception as e:
        print(f"⚠️ Erro ao obter detalhes de espécie: {e}")
        return None, None, None


def _traduzir_cacheado(texto: str, destino: str = "pt") -> str:
    """Traduz texto com cache interno."""
    if not texto:
        return texto

    cache_key = f"traducao_{texto}_{destino}"
    if traducao := cache.get(cache_key):
        return traducao

    traduzido = traduzir_texto(texto, destino)
    cache.set(cache_key, traduzido or texto, CACHE_TTL)
    return traduzido or texto
