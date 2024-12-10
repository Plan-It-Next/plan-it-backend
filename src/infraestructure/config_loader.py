from dotenv import load_dotenv
import os
import pathlib

# Ruta absoluta al archivo .env
ruta_env = pathlib.Path(__file__).resolve().parents[2] / ".env"

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=ruta_env)


def cargar_configuracion():
    # Obtener la clave de la API desde las variables de entorno
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError(f"La clave de la API no está configurada. Verifica el archivo .env en: {ruta_env}")

    return api_key