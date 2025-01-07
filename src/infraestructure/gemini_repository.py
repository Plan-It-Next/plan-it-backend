import google.generativeai as genai
import pandas as pd
import re
from pathlib import Path

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
        Extrae ciudades mencionadas en el texto a partir del archivo `world-cities.csv`
        y genera un prompt para obtener actividades o lugares típicos en dichas ciudades.

        :param texto: String que contiene información sobre ciudades o países.
        :return: String con actividades o lugares típicos para visitar en las ciudades detectadas.
        """
        # Cargar la lista de ciudades desde el archivo CSV
        # Definir la ruta al archivo
        archivo_ciudades = Path(__file__).parent / "world-cities.csv"
        # Comprobar si el archivo existe
        if archivo_ciudades.exists():
            ciudades_df = pd.read_csv(archivo_ciudades)
            ciudades_europeas = set(ciudades_df['name'].tolist())  # Convertir a un conjunto para búsquedas rápidas
        else:
            raise FileNotFoundError(f"El archivo 'world-cities.csv' no se encuentra en {archivo_ciudades}")

        # Extraer palabras del texto y normalizarlas
        palabras_texto = re.findall(r'\b\w+\b', texto)
        palabras_texto = [palabra.capitalize() for palabra in palabras_texto]

        # Identificar las ciudades mencionadas en el texto
        ciudades_detectadas = list(set(palabras_texto) & ciudades_europeas)
        if not ciudades_detectadas:
            raise ValueError("No se detectaron ciudades en el texto proporcionado.")

        # Crear el mensaje para Gemini con las ciudades detectadas
        mensaje = (
            f"Proporciona en español actividades o lugares típicos para visitar en las siguientes ciudades: "
            f"{', '.join(ciudades_detectadas)}. "
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
