import requests
import json
from wiki_engine import buscar_en_wikipedia
from decision_logic import DecisionEngine

class PixelText:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama3:8b-instruct-q2_K"
        self.engine = DecisionEngine()
        self.empresa = "Pacure Labs"

    def _llamar_ollama(self, prompt, sistema=""):
        """Comunicación directa con Ollama."""
        payload = {
            "model": self.model,
            "prompt": f"System: {sistema}\nUser: {prompt}\nAssistant:",
            "stream": False,
            "options": {"temperature": 0.2, "num_ctx": 2048}
        }
        try:
            response = requests.post(self.api_url, json=payload)
            return response.json().get('response', "").strip()
        except:
            return "ERROR_CONEXION"

    def cuestionar_respuesta(self, respuesta, contexto):
        """Sistema de autocrítica para evitar alucinaciones."""
        print("🛡️ [Pixel-text] Verificando integridad de la respuesta...")
        prompt_critica = (
            f"Contexto: {contexto}\n"
            f"Respuesta: {respuesta}\n"
            "Pregunta: ¿La respuesta contradice el contexto o inventa datos? Responde solo 'SI' o 'NO'."
        )
        critica = self._llamar_ollama(prompt_critica, "Eres un verificador de hechos estricto.")
        return "SI" in critica.upper()

    def procesar(self, entrada):
        decision = self.engine.clasificar(entrada)
        
        # FLUJO 1: Saludos y Social
        if decision == "MODO_SOCIAL":
            return f"¡Hola! Soy Pixel-text de {self.empresa}. Mi base de datos está lista para investigar."

        # FLUJO 2: Creatividad (Historias)
        if decision == "MODO_CREATIVO":
            print("📖 Generando relato creativo...")
            return self._llamar_ollama(entrada, "Eres un escritor creativo. Puedes imaginar cosas.")

        # FLUJO 3: Investigación (Veracidad obligatoria)
        if decision == "MODO_INVESTIGACION":
            datos = buscar_en_wikipedia(entrada)
            
            if not datos:
                return "No lo sé por ahora, pero lo buscaré en otras fuentes."

            contexto = datos['resumen']
            fuente = datos['fuente']
            
            # Intento 1
            instruccion = f"Responde usando SOLO este contexto: {contexto}. Si no sabes, di 'No lo sé'."
            respuesta = self._llamar_ollama(entrada, instruccion)

            # Revisión de alucinación
            if self.cuestionar_respuesta(respuesta, contexto):
                print("⚠️ Alucinación detectada. Corrigiendo...")
                respuesta = self._llamar_ollama(
                    f"Corrige esta respuesta basándote solo en el contexto: {contexto}",
                    "Eres un asistente que no tiene permitido inventar nada."
                )

            return f"{respuesta}\n\n[Fuente: {fuente} | {self.empresa}]"

        # Por defecto: Charla normal
        return self._llamar_ollama(entrada, f"Eres Pixel-text de {self.empresa}.")

# Lanzador
if __name__ == "__main__":
    bot = PixelText()
    print(f"--- Pixel-text por {bot.empresa} iniciado ---")
    while True:
        u = input("Tú: ")
        if u.lower() in ["exit", "salir"]: break
        print(f"Pixel-text: {bot.procesar(u)}\n")
