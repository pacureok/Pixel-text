import requests
import json

class DecisionLogic:
    def __init__(self, model="llama3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def identificar_peticion(self, user_input):
        """Usa Ollama para decidir si la pregunta es FACTUAL (buscar) o CREATIVA (charla)."""
        prompt = f"""
        Analiza la siguiente petición del usuario: "{user_input}"
        Clasifícala en una de estas dos categorías:
        1. BUSCAR: Si el usuario pregunta por definiciones, historia, ciencia o datos reales.
        2. CHAT: Si es un saludo, una opinión o pide crear un cuento/poema.
        
        Responde ÚNICAMENTE con la palabra 'BUSCAR' o 'CHAT'.
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload)
            result = response.json().get("response", "").strip().upper()
            
            # Limpieza básica por si el modelo responde con más texto
            if "BUSCAR" in result:
                return "BUSCAR"
            return "CHAT"
        except Exception as e:
            print(f"Error de conexión con Ollama: {e}")
            return "CHAT" # Por defecto charlar si falla la lógica
