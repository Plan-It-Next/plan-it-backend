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
        # Definir la ruta al archivo
        archivo_ciudades = Path(__file__).parent / "world-cities.csv"

        # Comprobar si el archivo existe
        if not archivo_ciudades.exists():
            raise FileNotFoundError(f"El archivo 'world-cities.csv' no se encuentra en {archivo_ciudades}")

        # Cargar la lista de ciudades desde el archivo CSV y convertir a un conjunto de nombres en minúsculas
        ciudades_df = pd.read_csv(archivo_ciudades)
        ciudades_europeas = set(ciudades_df['name'].str.lower())  # Convertir nombres de ciudades a minúsculas

        # Lista de palabras comunes que no deben interpretarse como ciudades
        palabras_prohibidas = {
            "hola", "gracias", "por", "favor", "quiero", "ir", "viajar", "destino", "gusto",
            "ver", "hacer", "lugares", "turismo", "plan", "recomendar", "puedo", "me", "un",
            "conocer", "estoy", "desde", "en", "a", "y", "el", "la", "los", "las", "de", "del",
            "para", "que", "una", "este", "ese", "ese", "si", "no"
        }

        # Extraer palabras del texto, normalizarlas a minúsculas y filtrar solo las que están en el conjunto de ciudades
        palabras_texto = re.findall(r'\b\w+\b', texto.lower())  # Extraer palabras y pasarlas a minúsculas
        palabras_filtradas = [palabra for palabra in palabras_texto if palabra not in palabras_prohibidas]
        ciudades_detectadas = list(set(palabras_filtradas) & ciudades_europeas)  # Intersección con ciudades

        # Verificar si se detectaron ciudades
        if not ciudades_detectadas:
            raise ValueError("No se detectaron ciudades en el texto proporcionado.")

        # Crear el mensaje para Gemini con las ciudades detectadas
        mensaje = (
            f"Proporciona, en español actividades o lugares típicos para visitar en las siguientes ciudades: "
            f"{', '.join(ciudades_detectadas)}. "
            "El resultado debe ser un texto breve y directo, señalando las cosas típicas del lugar y a poder ser algo especial y único que se pueda hacer en ese sitio, así como también si se nombra algún plato típico estaría bien añadir algún sitio real que tenga buenas reseñas para probarlo"
        )

        # Enviar el mensaje al modelo
        chat = self.model.start_chat(history=[])
        response = chat.send_message(mensaje)

        # Verificar y devolver el texto de respuesta sin negritas
        try:
            respuesta = response.text.strip()
            respuesta_sin_negritas = re.sub(r'\*\*(.*?)\*\*', r'\1', respuesta)  # Elimina cualquier negrita en Markdown
            return respuesta_sin_negritas
        except Exception as e:
            raise ValueError(f"Error al procesar la respuesta de Gemini: {e}")