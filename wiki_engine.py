import wikipedia

class WikiEngine:
    def __init__(self):
        wikipedia.set_lang("es")

    def buscar(self, query):
        try:
            # Intento 1: Resumen directo
            return wikipedia.summary(query, sentences=3)
        except:
            try:
                # Intento 2: Búsqueda y primer resultado
                busqueda = wikipedia.search(query)
                if busqueda:
                    return wikipedia.summary(busqueda[0], sentences=3)
                return None
            except:
                return None
