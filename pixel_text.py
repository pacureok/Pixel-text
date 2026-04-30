from wiki_engine import WikiEngine
from decision_logic import DecisionLogic

class PixelText:
    def __init__(self):
        self.brain = DecisionLogic()
        self.wiki = WikiEngine()

    def procesar(self, user_input):
        # 1. Identificar qué quiere el usuario
        intencion = self.brain.identificar_peticion(user_input)
        
        contexto_extra = ""
        
        # 2. Si es factual, traemos datos de Wikipedia
        if intencion == "factual":
            datos_reales = self.wiki.buscar(user_input)
            if datos_reales:
                contexto_extra = f"\nUsa esta información real para tu respuesta: {datos_reales}"
        
        # 3. Generar la respuesta final con Llama-3 usando el contexto (si existe)
        respuesta_final = self.generar_con_ollama(user_input, contexto_extra, intencion)
        return respuesta_final

    def generar_con_ollama(self, prompt, contexto, intencion):
        # Aquí haces la llamada final a Ollama para que redacte
        # Si contexto tiene datos de Wikipedia, la respuesta será veraz.
        pass
