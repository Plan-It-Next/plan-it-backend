from fastapi import APIRouter, HTTPException
from src.application.planning_service import PlanningService
from src.infraestructure.gemini_repository import GeminiRepository
from src.infraestructure.config_loader import cargar_configuracion
import pathlib
import os

# Cargar la clave de la API desde el archivo .env
api_key = cargar_configuracion()

gemini_repo = GeminiRepository(api_key=api_key)

# Instanciar el servicio
planning_service = PlanningService(gemini_repo)

# Crear el router
router = APIRouter()

@router.post("/planning")
async def obtener_planning(ciudad: str, fecha_ini: str, fecha_fin: str):
    try:
        # Llamar al servicio
        resultado = planning_service.obtener_planning(ciudad, fecha_ini, fecha_fin)
        return {"planning": resultado}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")