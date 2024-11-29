import yaml
import os

# Función para cargar configuraciones desde un archivo YAML
def cargar_configuracion(ruta_archivo: str) -> str:
    with open(ruta_archivo, 'r') as archivo:
        datos = yaml.safe_load(archivo)
    clave_api = datos.get('api')
    if not clave_api:
        raise ValueError("La clave 'api' no se encontró en el archivo de configuración.")
    return clave_api