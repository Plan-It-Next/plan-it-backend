from ..infraestructure.gemini_repository import GeminiRepository


class PlanningService:
    def __init__(self, gemini_repository: GeminiRepository):
        self.gemini_repository = gemini_repository

    def obtener_planning(self, ciudad: str, fecha_ini: str, fecha_fin: str) -> dict:
        # Lógica de negocio o validaciones adicionales
        if not ciudad or not fecha_ini or not fecha_fin:
            raise ValueError("Los parámetros ciudad, fecha_ini y fecha_fin son obligatorios.")

        return self.gemini_repository.obtener_planning(ciudad, fecha_ini, fecha_fin)