import requests
import json

class DecisionLogic:
    def __init__(self, model="llama3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def identificar_peticion(self, prompt):
        """Usa Ollama para clasificar la intención del usuario."""
        instruccion_sistema = (
            "Eres un clasificador de intenciones. Responde UNICAMENTE con una palabra:\n"
            "- 'FACTUAL': si el usuario pide información real, ciencia, historia o definiciones.\n"
            "- 'CREATIVO': si el usuario pide cuentos, poemas, chistes o rol.\n"
            "- 'SALUDO': si es solo un hola o presentación.\n"
            f"Usuario dice: {prompt}"
        )

        payload = {
            "model": self.model,
            "prompt": instruccion_sistema,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload)
            # Extraemos la categoría limpia
            categoria = response.json().get("response", "").strip().upper()
            
            # Limpieza básica por si el modelo se pone charlatán
            if "FACTUAL" in categoria: return "factual"
            if "CREATIVO" in categoria: return "creativo"
            return "saludo"
            
        except Exception as e:
            print(f"Error conectando con Ollama: {e}")
            return "factual" # Por defecto intentamos buscar datos si falla la lógica
