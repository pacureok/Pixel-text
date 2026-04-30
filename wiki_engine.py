import wikipediaapi

class WikiEngine:
    def __init__(self):
        # Es CRÍTICO identificarse ante Wikipedia para evitar bloqueos
        self.wiki = wikipediaapi.Wikipedia(
            language='es',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='PixelTextBot/1.0 (pacurelabs@example.com)'
        )

    def buscar(self, consulta):
        """Busca información real en Wikipedia."""
        try:
            # Primero intentamos la búsqueda directa
            pagina = self.wiki.page(consulta)
            
            if pagina.exists():
                # Retornamos el resumen (primeros 600 caracteres)
                return f"Información técnica de Wikipedia: {pagina.summary[:600]}..."
            
            # Si no existe, intentamos buscar sugerencias de títulos similares
            # (Nota: wikipedia-api no busca por 'keyword' tan bien como la API de MediaWiki, 
            # pero para términos generales como 'Agujero Negro' funciona perfecto)
            return None
            
        except Exception as e:
            print(f"Error en WikiEngine: {e}")
            return None
