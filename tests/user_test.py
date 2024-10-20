import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_all_users_returns_all_users():
    users_expected = [
        {"name": "Juan Pérez", "email": "juan.perez@example.com"},
        {"name": "María López", "email": "maria.lopez@example.com"},
        {"name": "Carlos García", "email": "carlos.garcia@example.com"},
        {'name': 'Ana Sánchez', 'email': 'ana.sanchez@example.com'},
        {'name': 'Pedro Martínez', 'email': 'pedro.martinez@example.com'}
    ]

    response = client.get("/users")
    response_json = response.json()
    response_filtered = [{"name": user["name"], "email": user["email"]} for user in response_json]


    assert response.status_code == 200
    for user in users_expected:
        assert user in response_filtered


def test_get_user_by_id_returns_user():
    user_expected = {'user_id': '5513721c-1e99-447c-90a1-640bef82b834', 'name': 'Ana Sánchez', 'email': 'ana.sanchez@example.com'}
    user_id = '5513721c-1e99-447c-90a1-640bef82b834'

    response = client.get(f"/users/user/{user_id}")
    response_json = response.json()

    assert  response.status_code == 200
    assert user_expected == response_json

def test_get_user_by_id_throws_exception_no_user():
    #user_id no existe
    user_id = '5513721c-1e99-447c-90a1-640bef82b835'

    response = client.get(f"/users/user/{user_id}")
    response_json = response.json()

    assert response.status_code == 404
    assert response_json['detail'] == f"User with ID {user_id} not found"

def test_get_user_by_id_throws_exception_invalid_uuid():
    #user_id wrong format
    user_id = '5513721c-1e99-447c-90a1-640bef82b83'

    response = client.get(f"/users/user/{user_id}")
    response_json = response.json()

    assert response.status_code == 422

def test_get_users_by_group_id_returns_users():
    users_expected = [
        {"name": "Juan Pérez", "email": "juan.perez@example.com"},
        {"name": "Carlos García", "email": "carlos.garcia@example.com"}
    ]
    group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c'

    response = client.get(f"/users/{group_id}")
    response_json = response.json()
    response_filtered = [{"name": user["name"], "email": user["email"]} for user in response_json]

    assert response.status_code == 200
    for user in users_expected:
        assert user in response_filtered

def test_get_users_by_group_id_throws_exception_no_users():
    # group_id no existe
    group_id = '3864dfc4-c9ca-4929-966e-717e7269e69d'

    response = client.get(f"/users/{group_id}")
    response_json = response.json()

    assert response.status_code == 404
    assert response_json['detail'] == f"No users found"