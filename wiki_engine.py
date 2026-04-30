import requests

def buscar_en_wikipedia(tema):
    """
    Busca un resumen veraz en Wikipedia. 
    Si no encuentra nada, devuelve None para activar el modo 'No lo sé'.
    """
    # Limpiamos el tema para la URL
    tema_clean = tema.title().replace(" ", "_")
    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{tema_clean}"
    
    headers = {
        'User-Agent': 'Pixel-text_Bot/1.0 (Pacure_Labs_Contact)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "resumen": data.get('extract'),
                "url": data.get('content_urls', {}).get('desktop', {}).get('page')
            }
        return None
    except Exception:
        return None
