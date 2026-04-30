import requests
from wiki_engine import buscar_en_wikipedia
from decision_logic import clasificar_intencion

class PixelText:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama3:8b-instruct-q2_K"

    def responder(self, prompt):
        intencion = clasificar_intencion(prompt)
        
        # CASO 1: SALUDO
        if intencion == "saludo":
            return "¡Hola! Soy Pixel-text de Pacure Labs. Estoy listo para investigar o charlar."

        # CASO 2: HISTORIA (Normal, sin Wikipedia)
        if intencion == "historia":
            return self._consultar_ollama(f"Sé creativo y cuéntame: {prompt}")

        # CASO 3: INVESTIGACIÓN (Usa Wikipedia)
        if intencion == "investigacion":
            datos = buscar_en_wikipedia(prompt)
            if datos:
                contexto = f"Información real encontrada: {datos['resumen']}"
                instruccion = f"Basándote en esto: {contexto}, responde a: {prompt}. Sé breve y exacto."
                return self._consultar_ollama(instruccion)
            else:
                return "No lo sé con certeza, pero lo buscaré en otras fuentes más adelante."

        # CASO 4: CHARLA NORMAL
        return self._consultar_ollama(prompt)

    def _consultar_ollama(self, system_prompt):
        payload = {"model": self.model, "prompt": system_prompt, "stream": False}
        try:
            r = requests.post(self.api_url, json=payload)
            return r.json().get('response', "Error en el cerebro.")
        except:
            return "Error: Asegúrate de que Ollama esté corriendo."

if __name__ == "__main__":
    bot = PixelText()
    print("--- Pixel-text (Versión Pacure Labs) ---")
    while True:
        u = input(">> ")
        print(f"IA: {bot.responder(u)}\n")
