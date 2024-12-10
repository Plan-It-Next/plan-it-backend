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