from fastapi.testclient import TestClient
from src.api.main import app
from unittest import mock

client = TestClient(app)


def test_post_planning_returns_planning():
    # Respuesta esperada del endpoint
    planning_expected = {
        "planning": {
            "day1": "Visita al museo",
            "day2": "Caminata en el parque"
        }
    }

    # Simular el comportamiento de PlanningService
    with mock.patch('src.application.planning_service.PlanningService.obtener_planning', return_value=planning_expected["planning"]):
        # Enviar la solicitud POST al endpoint
        response = client.post("/planning", params={
            "ciudad": "Madrid",
            "fecha_ini": "2024-01-01",
            "fecha_fin": "2024-01-05"
        })

        # Verificar el código de respuesta y el contenido
        assert response.status_code == 200
        assert response.json() == planning_expected


def test_post_planning_throws_exception_bad_request():
    # Simular un ValueError lanzado por PlanningService
    with mock.patch('src.application.planning_service.PlanningService.obtener_planning', side_effect=ValueError("Los parámetros ciudad, fecha_ini y fecha_fin son obligatorios.")):
        # Enviar la solicitud POST al endpoint con parámetros faltantes
        response = client.post("/planning", params={
            "ciudad": "",
            "fecha_ini": "2024-01-01",
            "fecha_fin": "2024-01-05"
        })

        # Verificar el código de respuesta y el mensaje de error
        assert response.status_code == 400
        assert response.json()["detail"] == "Los parámetros ciudad, fecha_ini y fecha_fin son obligatorios."


def test_post_planning_throws_exception_internal_error():
    # Simular un error genérico lanzado por PlanningService
    with mock.patch('src.application.planning_service.PlanningService.obtener_planning', side_effect=Exception("Error interno")):
        # Enviar la solicitud POST al endpoint
        response = client.post("/planning", params={
            "ciudad": "Madrid",
            "fecha_ini": "2024-01-01",
            "fecha_fin": "2024-01-05"
        })

        # Verificar el código de respuesta y el mensaje de error
        assert response.status_code == 500
        assert response.json()["detail"] == "Error interno del servidor"
