from wiki_engine import WikiEngine
from decision_logic import DecisionLogic
import requests

class PixelText:
    def __init__(self):
        self.wiki = WikiEngine()
        self.logic = DecisionLogic()
        self.model_url = "http://localhost:11434/api/generate"

    def procesar(self, prompt):
        # 1. Identificar qué quiere el usuario
        categoria = self.logic.identificar_peticion(prompt)
        
        contexto_extra = ""
        if categoria == "BUSCAR":
            print(f"🔍 Detectada petición factual. Buscando en Wikipedia...")
            datos = self.wiki.buscar(prompt)
            if datos:
                contexto_extra = f"\nUsa estos datos reales para tu respuesta: {datos}"
        
        # 2. Generar la respuesta final con el LLM
        full_prompt = f"Instrucción: Responde de forma amable y precisa en español.{contexto_extra}\nUsuario: {prompt}"
        
        payload = {
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False
        }

        response = requests.post(self.model_url, json=payload)
        return response.json().get("response", "Lo siento, tuve un error interno.")

# --- EJECUCIÓN ---
bot = PixelText()
print(bot.procesar("¿Qué es un agujero negro?"))
