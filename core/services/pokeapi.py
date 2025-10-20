import requests
from django.core.cache import cache

POKEAPI_BASE = "https://pokeapi.co/api/v2"
CACHE_TIMEOUT = 60 * 60 * 24  # 24h


def _get_json(url: str):
    """Executa requisições seguras à PokéAPI com cache e logs de erro."""
    cache_key = f"pokeapi_cache:{url}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, timeout=CACHE_TIMEOUT)
            return data
        print(f"⚠️ Erro {response.status_code} ao acessar {url}")
    except requests.RequestException as e:
        print(f"❌ Falha na requisição: {e}")

    # Se der erro, tenta retornar o último cache válido (mesmo expirado)
    old_data = cache.get(cache_key)
    if old_data:
        print("⚙️ Retornando dados antigos do cache.")
        return old_data

    return None


def buscar_pokemon_da_pokeapi(nome: str):
    """Retorna os dados básicos de um Pokémon."""
    return _get_json(f"{POKEAPI_BASE}/pokemon/{nome.lower()}")


def buscar_geracao_do_pokemon(nome: str):
    """Obtém o número da geração de um Pokémon."""
    dados = _get_json(f"{POKEAPI_BASE}/pokemon-species/{nome.lower()}")
    if not dados:
        return None

    url_geracao = dados.get("generation", {}).get("url")
    if not url_geracao:
        return None

    try:
        return int(url_geracao.strip("/").split("/")[-1])
    except (ValueError, AttributeError):
        return None
