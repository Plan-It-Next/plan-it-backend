import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from httpx import AsyncClient
from fastapi import status


client = TestClient(app)

@pytest.fixture
def get_token():
    user = 'juan.perez@example.com'
    passw = 'juanperez123'
    response = client.post(f"/login/{user}/{passw}")
    return response.json()["access_token"]


def test_get_all_users_returns_all_users(get_token):
    users_expected = [
        {"name": "Juan Pérez", "email": "juan.perez@example.com"},
        {"name": "María López", "email": "maria.lopez@example.com"},
        {"name": "Carlos García", "email": "carlos.garcia@example.com"},
        {'name': 'Ana Sánchez', 'email': 'ana.sanchez@example.com'},
        {'name': 'Pedro Martínez', 'email': 'pedro.martinez@example.com'}
    ]

    headers = {"Authorization": f"Bearer {get_token}"}

    response = client.get("/users", headers=headers)
    response_json = response.json()
    response_filtered = [{"name": user["name"], "email": user["email"]} for user in response_json]


    assert response.status_code == 200
    for user in users_expected:
        assert user in response_filtered


def test_get_user_by_id_returns_user(get_token):
    user_expected = {'user_id': '5513721c-1e99-447c-90a1-640bef82b834', 'name': 'Ana Sánchez', 'email': 'ana.sanchez@example.com'}
    user_id = '5513721c-1e99-447c-90a1-640bef82b834'
    headers = {"Authorization": f"Bearer {get_token}"}

    response = client.get(f"/users/user/{user_id}", headers=headers)
    response_json = response.json()

    assert  response.status_code == 200
    assert user_expected == response_json

def test_get_user_by_id_throws_exception_no_user(get_token):
    #user_id no existe
    user_id = '5513721c-1e99-447c-90a1-640bef82b835'
    headers = {"Authorization": f"Bearer {get_token}"}

    response = client.get(f"/users/user/{user_id}", headers=headers)
    response_json = response.json()

    assert response.status_code == 404
    assert response_json['detail'] == f"User with ID {user_id} not found"

def test_get_user_by_id_throws_exception_invalid_uuid(get_token):
    #user_id wrong format
    user_id = '5513721c-1e99-447c-90a1-640bef82b83'
    headers = {"Authorization": f"Bearer {get_token}"}

    response = client.get(f"/users/user/{user_id}", headers=headers)
    response_json = response.json()

    assert response.status_code == 422

def test_get_users_by_group_id_returns_users(get_token):
    users_expected = [
        {"name": "Juan Pérez", "email": "juan.perez@example.com"},
        {"name": "Carlos García", "email": "carlos.garcia@example.com"}
    ]
    group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c'
    headers = {"Authorization": f"Bearer {get_token}"}

    response = client.get(f"/users/{group_id}", headers=headers)
    response_json = response.json()
    response_filtered = [{"name": user["name"], "email": user["email"]} for user in response_json]

    assert response.status_code == 200
    for user in users_expected:
        assert user in response_filtered

def test_get_users_by_group_id_throws_exception_no_users(get_token):
    # group_id no existe
    group_id = '3864dfc4-c9ca-4929-966e-717e7269e69d'
    headers = {"Authorization": f"Bearer {get_token}"}

    response = client.get(f"/users/{group_id}", headers=headers)
    response_json = response.json()

    assert response.status_code == 404
    assert response_json['detail'] == f"No users found"