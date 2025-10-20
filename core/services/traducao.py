from django.core.cache import cache
import requests
from functools import lru_cache

@lru_cache(maxsize=512)
def traduzir_texto(texto: str, destino: str = "pt") -> str:
    if not texto:
        return texto

    cache_key = f"traducao_{texto}_{destino}"
    if cache.get(cache_key):
        return cache.get(cache_key)

    try:
        resp = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": texto, "langpair": f"en|{destino}"},
            timeout=6,
        )
        if resp.status_code == 200:
            data = resp.json()
            traduzido = data.get("responseData", {}).get("translatedText", texto)
            cache.set(cache_key, traduzido, 60 * 60 * 24)
            return traduzido
    except:
        pass
    return texto
