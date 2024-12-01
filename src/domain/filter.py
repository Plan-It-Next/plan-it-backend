from pydantic import BaseModel
from typing import Optional
from datetime import date


class TripFilter(BaseModel):
    # Filtros para los nodos de estación
    ciudad_origen: Optional[str] = None
    ciudad_destino: Optional[str] = None
    pais: Optional[str] = None
    tipo_ruta: Optional[str] = None
    fecha: Optional[str] = None
    # Filtros para las aristas (rutas)
    precio_billete: Optional[float] = None
    distancia: Optional[float] = None
    duracion: Optional[int] = None