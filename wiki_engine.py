import wikipediaapi

class WikiEngine:
    def __init__(self, language='es'):
        # Es CRUCIAL tener un user_agent para que Wikipedia no bloquee la conexión
        self.wiki = wikipediaapi.Wikipedia(
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent="PixelTextBot/1.0 (https://github.com/pacureok/Pixel-text; pacurelabs@example.com)"
        )

    def buscar(self, query):
        """Busca un resumen en Wikipedia para alimentar al LLM."""
        try:
            # Intentar obtener la página
            page = self.wiki.page(query)
            
            if page.exists():
                # Retornamos los primeros 600 caracteres para no saturar el contexto
                # pero dar suficiente información técnica.
                return f"Información encontrada en Wikipedia sobre {query}: {page.summary[:600]}..."
            
            # Si no existe, intentar una búsqueda más genérica (opcional)
            return None
        except Exception as e:
            print(f"Error en WikiEngine: {e}")
            return None
