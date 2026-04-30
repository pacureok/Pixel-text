import requests

def buscar_en_wikipedia(consulta):
    """
    Motor de búsqueda de Pacure Labs para Wikipedia.
    Busca el título más relevante y extrae su resumen.
    """
    print(f"🔍 [Pixel-text] Investigando en Wikipedia: {consulta}...")
    
    # 1. Buscar el título del artículo más cercano
    search_url = "https://es.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": consulta,
        "format": "json",
        "utf8": 1
    }

    try:
        # Petición de búsqueda
        res_search = requests.get(search_url, params=search_params, timeout=5)
        search_data = res_search.json()
        resultados = search_data.get("query", {}).get("search", [])

        if not resultados:
            return None

        # Tomamos el título del primer resultado (el más relevante)
        titulo_oficial = resultados[0]['title']

        # 2. Obtener el resumen (REST API)
        summary_url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{titulo_oficial.replace(' ', '_')}"
        res_summary = requests.get(summary_url, timeout=5)
        
        if res_summary.status_code == 200:
            data = res_summary.json()
            return {
                "titulo": titulo_oficial,
                "resumen": data.get('extract'),
                "fuente": data.get('content_urls', {}).get('desktop', {}).get('page')
            }
    except Exception as e:
        print(f"❌ Error en Wiki-Engine: {e}")
        return None
    
    return None
