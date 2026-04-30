import re

class DecisionEngine:
    def __init__(self):
        # Patrones de texto para decisiones rápidas y precisas
        self.patterns = {
            "saludo": r"\b(hola|buenos días|buenas|qué tal|saludos|hey)\b",
            "historia": r"\b(cuéntame|inventa|crea|narra|escribe|historia|relato|cuento)\b",
            "investigacion": r"\b(quién|qué es|cómo|cuándo|dónde|por qué|explica|define|datos|historia de|biografía)\b"
        }

    def limpiar_texto(self, texto):
        """Limpia el texto para una clasificación sin errores."""
        texto = texto.lower().strip()
        # Elimina signos de puntuación innecesarios para el análisis
        return re.sub(r'[^\w\s\?]', '', texto)

    def clasificar(self, entrada_usuario):
        """
        Analiza la entrada y toma una decisión ejecutiva sobre qué flujo seguir.
        """
        texto = self.limpiar_texto(entrada_usuario)
        
        # 1. Prioridad: ¿Es una petición creativa? (Historias)
        # Si el usuario pide "inventar", ignoramos los datos fácticos para dar libertad a la IA.
        if re.search(self.patterns["historia"], texto):
            return "MODO_CREATIVO"

        # 2. ¿Es una duda sobre el mundo real? (Investigación)
        # Si hay signos de interrogación o palabras de consulta, activamos Wikipedia.
        if re.search(self.patterns["investigacion"], texto) or "?" in entrada_usuario:
            return "MODO_INVESTIGACION"

        # 3. ¿Es interacción social básica? (Saludo)
        if re.search(self.patterns["saludo"], texto):
            return "MODO_SOCIAL"

        # 4. Decisión por defecto: Charla normal
        # Si no encaja en nada, se trata como conversación fluida.
        return "MODO_CHAT"

    def requiere_busqueda(self, categoria):
        """Retorna True si la decisión tomada requiere el uso de Wikipedia."""
        return categoria == "MODO_INVESTIGACION"
