import wikipedia

class WikiEngine:
    def __init__(self):
        # Configurar el idioma a español globalmente
        wikipedia.set_lang("es")

    def buscar(self, query):
        try:
            # 1. Intentar obtener el resumen directo
            return wikipedia.summary(query, sentences=3)
        except (wikipedia.DisambiguationError, wikipedia.PageError):
            try:
                # 2. Si falla, buscar páginas relacionadas
                resultados = wikipedia.search(query)
                if resultados:
                    # Intentar con el primer resultado de la lista
                    return wikipedia.summary(resultados[0], sentences=3)
                return None
            except:
                return None
