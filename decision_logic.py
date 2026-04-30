import requests
from wiki_engine import WikiEngine

class PixelText:
    def __init__(self):
        self.wiki = WikiEngine()
        self.ollama_url = "http://localhost:11434/api/generate"

    def procesar(self, user_input):
        # Primero intentamos obtener datos reales
        datos_wiki = self.wiki.buscar(user_input)
        
        if not datos_wiki:
            # Si no hay datos en Wikipedia, dejamos que Ollama responda con su lógica interna
            contexto = "Responde de forma creativa o general."
        else:
            # Si hay datos, se los inyectamos a Ollama para que NO diga "No lo sé"
            contexto = f"Basándote en esta información de Wikipedia: {datos_wiki}, responde al usuario."

        # Construcción del prompt final para Ollama
        prompt_final = f"Instrucción: {contexto}\nUsuario: {user_input}\nPixel-text:"

        payload = {
            "model": "llama3",
            "prompt": prompt_final,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload)
            return response.json().get("response", "Error al generar respuesta.")
        except Exception as e:
            return f"Error de conexión con el servidor: {e}"

# --- PRUEBA DE FUEGO ---
bot = PixelText()
print(bot.procesar("¿Qué es un agujero negro?"))
