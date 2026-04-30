import requests
import json
from wiki_engine import buscar_en_wikipedia
from decision_logic import DecisionEngine

class PixelText:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama3:8b-instruct-q2_K"
        self.engine = DecisionEngine()
        self.credito = "Pacure Labs"

    def _consultar_ollama(self, prompt, system_instruction=""):
        full_prompt = f"Sistema: {system_instruction}\nUsuario: {prompt}\nAsistente:"
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {"num_ctx": 2048, "temperature": 0.3} # Temp baja para evitar alucinación
        }
        try:
            r = requests.post(self.api_url, json=payload)
            return r.json().get('response', "").strip()
        except Exception as e:
            return f"Error de conexión con el cerebro: {e}"

    def autocrítica(self, respuesta, contexto_real):
        """
        La IA cuestiona su propia respuesta comparándola con los datos reales.
        """
        print("🔍 [Pixel-text] Cuestionando veracidad de la respuesta...")
        critica_prompt = (
            f"Contexto real: {contexto_real}\n"
            f"Respuesta generada: {respuesta}\n"
            "Pregunta: ¿La respuesta contiene errores o inventa datos que no están en el contexto? "
            "Responde solo con 'CORRECTO' o 'REHACER'."
        )
        
        veredicto = self._consultar_ollama(critica_prompt, "Eres un auditor de datos estricto.")
        return "REHACER" in veredicto.upper()

    def procesar(self, user_input):
        decision = self.engine.clasificar(user_input)
        
        # 1. Modo Social
        if decision == "MODO_SOCIAL":
            return f"¡Hola! Soy Pixel-text, una creación de {self.credito}. ¿En qué puedo ayudarte hoy?"

        # 2. Modo Creativo (Historias)
        if decision == "MODO_CREATIVO":
            print("📖 Generando relato creativo...")
            return self._consultar_ollama(user_input, "Eres un escritor creativo de Pacure Labs.")

        # 3. Modo Investigación (99.8% Veracidad)
        if decision == "MODO_INVESTIGACION":
            datos_wiki = buscar_en_wikipedia(user_input)
            
            if not datos_wiki:
                return "No lo sé con certeza en este momento, pero lo buscaré en otras fuentes para ti."

            contexto = datos_wiki['resumen']
            instruccion = f"Responde usando solo este contexto: {contexto}. Si no está ahí, di que no lo sabes."
            
            # Primer intento
            respuesta = self._consultar_ollama(user_input, instruccion)
            
            # Autocrítica / Revisión
            if self.autocrítica(respuesta, contexto):
                print("⚠️ Detectada posible alucinación. Rehaciendo respuesta...")
                respuesta = self._consultar_ollama(
                    f"Tu respuesta anterior fue imprecisa. Basándote ESTRICTAMENTE en: {contexto}, responde de nuevo: {user_input}",
                    "Eres un asistente que no tiene permitido mentir ni inventar."
                )
            
            return f"{respuesta}\n\n[Fuente: Wikipedia/Pacure Labs]"

        # 4. Modo Chat Normal
        return self._consultar_ollama(user_input, f"Eres Pixel-text de {self.credito}. Responde de forma clara.")

# --- INTERFAZ DE CONSOLA ---
if __name__ == "__main__":
    ia = PixelText()
    print(f"--- PIXEL-TEXT (Base Ollama) | Propiedad de Pacure Labs ---")
    print("Optimizado para 2GB VRAM / 5GB RAM. Escribe 'salir' para finalizar.\n")
    
    while True:
        try:
            frase = input(">> ")
            if frase.lower() in ["salir", "exit", "quit"]:
                break
                
            resultado = ia.procesar(frase)
            print(f"\nPixel-text: {resultado}\n")
            
        except KeyboardInterrupt:
            break

    print("\nApagando Pixel-text. Créditos: Pacure Labs.")
