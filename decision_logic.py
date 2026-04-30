
import requests
import pandas as pd
from ddgs import DDGS
import io
import re

class DecisionLogic:
    def __init__(self, model="llama3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def busqueda_web_profunda(self, query):
        try:
            with DDGS() as ddgs:
                resultados = [r['body'] for r in ddgs.text(query, max_results=3)]
                return "\n---\n".join(resultados)
        except:
            return "Datos web no disponibles."

    def generar_excel(self, datos_texto):
        """Limpia y convierte datos en un Excel con formato profesional."""
        try:
            # Prompt específico para obtener SOLO el CSV puro
            prompt_limpieza = f"""
            Basado en esta info: {datos_texto}
            Genera SOLO un texto en formato CSV usando coma ',' como separador. 
            Incluye encabezados. No escribas nada más, solo el código CSV.
            """
            payload = {"model": self.model, "prompt": prompt_limpieza, "stream": False}
            res = requests.post(self.url, json=payload).json().get("response", "")
            
            # Limpiar posibles bloques de código de Llama (```csv ... ```)
            csv_clean = re.sub(r'```.*?```', '', res, flags=re.DOTALL).strip()
            if "csv" in csv_clean.lower():
                csv_clean = csv_clean.lower().replace("csv", "").strip()

            # Leer y guardar
            df = pd.read_csv(io.StringIO(csv_clean))
            file_path = "/kaggle/working/Pixel-text/reporte_pixel.xlsx"
            
            # Aplicar estilo básico
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Analisis')
            
            return f"\n\n📊 **[SISTEMA] Excel generado con éxito:** `reporte_pixel.xlsx` en tu carpeta de trabajo."
        except Exception as e:
            return f"\n\n⚠️ Error al procesar Excel: {str(e)}"

    def procesar_con_ollama(self, prompt, contexto_wiki=None):
        # Decidir fuente de datos
        es_factual = any(palabra in prompt.lower() for palabra in ["que", "quien", "como", "tabla", "vs", "compar"])
        contexto = contexto_wiki if contexto_wiki else self.busqueda_web_profunda(prompt)

        prompt_maestro = f"""
        Eres Pixel-text de Pacure Labs.
        INSTRUCCIONES:
        1. Responde DIRECTO y en ESPAÑOL.
        2. Prohibido mencionar temas irrelevantes (series, personajes externos).
        3. Si hay datos de tablas, preséntalos en Markdown claro.
        
        DATOS: {contexto}
        USUARIO: {prompt}
        """

        try:
            payload = {"model": self.model, "prompt": prompt_maestro, "stream": False, "options": {"temperature": 0.1}}
            response = requests.post(self.url, json=payload).json().get("response", "")
            
            # Disparador de Excel
            if "tabla" in prompt.lower() or "comparación" in prompt.lower():
                response += self.generar_excel(contexto)
                
            return response
        except Exception as e:
            return f"Error: {e}"
