import requests
import json

class PixelText:
    def __init__(self):
        self.url_ollama = "http://localhost:11434/api/generate"
        self.model = "llama3:8b-instruct-q2_K" # Modelo ultra-ligero

    def buscar_wikipedia(self, tema):
        print(f"🔍 [Pixel-text] Buscando en Wikipedia...")
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{tema.replace(' ', '_')}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json().get('extract', "Sin datos.")
            return "No lo sé, pero lo buscaré..."
        except:
            return "Error de conexión al buscar."

    def procesar(self, entrada):
        user_input = entrada.lower()

        # 1. Identificar Saludos
        if any(s in user_input for s in ["hola", "buen día", "qué tal"]):
            return "¡Hola! Soy Pixel-text de Pacure Labs. ¿En qué te ayudo?"

        # 2. Identificar si quiere una Historia
        if "cuéntame una historia" in user_input or "inventa" in user_input:
            print("📖 Generando historia creativa...")
            return self.llamar_ollama(f"Escribe una historia creativa sobre: {entrada}")

        # 3. Pregunta Fáctica (Evitar alucinación)
        print("🛡️ Verificando veracidad...")
        contexto = self.buscar_wikipedia(entrada)
        
        if contexto == "No lo sé, pero lo buscaré...":
            return contexto

        prompt = f"Basado únicamente en este texto: '{contexto}', responde la pregunta: {entrada}. Si no está ahí, di que no lo sabes."
        return self.llamar_ollama(prompt)

    def llamar_ollama(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url_ollama, json=payload)
            return response.json().get('response', "Error en el cerebro.")
        except:
            return "Ollama no está iniciado. Por favor, corre 'ollama serve'."

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    bot = PixelText()
    print("--- Pixel-text por Pacure Labs (Base Ollama) ---")
    while True:
        user_text = input("Tú: ")
        if user_text.lower() in ["salir", "exit"]: break
        respuesta = bot.procesar(user_text)
        print(f"Pixel-text: {respuesta}\n")
