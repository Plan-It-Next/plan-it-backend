import google.generativeai as genai

class GeminiRepository:
    def __init__(self, api_key: str):
        # Configurar Gemini con la clave API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def obtener_planning(self, ciudad: str, fecha_ini: str, fecha_fin: str) -> dict:
        # Crear el mensaje para Gemini
        mensaje = (
            f"Dame un planning en español para hacer del {fecha_ini} al {fecha_fin} en la ciudad de {ciudad}. "
            "La respuesta debes devolverla en formato JSON."
        )
        # Enviar el mensaje al modelo
        chat = self.model.start_chat(history=[])
        response = chat.send_message(mensaje)

        # Asegurarnos de que la respuesta es un JSON válido
        try:
            return response.text
        except Exception as e:
            raise ValueError(f"Error al procesar la respuesta de Gemini: {e}")

    def obtener_actividades(self, texto: str) -> str:
        """
        Extrae la ciudad del texto proporcionado y genera un prompt para
        obtener actividades o lugares típicos para visitar en esa ciudad.

        :param texto: String que contiene información sobre una ciudad.
        :return: String con una actividad o lugar típico para visitar en la ciudad.
        """
        import re

        # Intentar extraer el nombre de una ciudad desde el texto
        # Puedes ajustar el regex según el idioma y el formato del texto
        match = re.search(r"\b(?:en|de|a|la ciudad de|ciudad de)\s+([A-Z][a-záéíóúñü]+(?:\s+[A-Z][a-záéíóúñü]+)?)",
                          texto)
        if not match:
            raise ValueError("No se pudo identificar una ciudad en el texto proporcionado.")

        ciudad = match.group(1)

        # Crear el mensaje para Gemini
        mensaje = (
            f"Proporciona en español una actividad o lugar típico para visitar en {ciudad}. "
            "El resultado debe ser un texto breve y directo."
        )

        # Enviar el mensaje al modelo
        chat = self.model.start_chat(history=[])
        response = chat.send_message(mensaje)

        # Verificar y devolver el texto de respuesta
        try:
            return response.text.strip()
        except Exception as e:
            raise ValueError(f"Error al procesar la respuesta de Gemini: {e}")
