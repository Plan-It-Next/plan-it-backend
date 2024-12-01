from fastapi.testclient import TestClient
from src.api.main import app
from unittest import mock

client = TestClient(app)

def test_get_all_groups_returns_all_groups():
    groups_expected = [
        {"name": "Grupo A", "budget": 1000.00},
        {"name": "Grupo B", "budget": 1500.50},
        {"name": "Grupo C", "budget": 2000}
    ]

    response = client.get("/groups")
    response_json = response.json()
    response_filtered = [{"name": group["name"], "budget": group["budget"]} for group in response_json]


    assert response.status_code == 200
    for user in groups_expected:
        assert user in response_filtered

def test_get_groups_by_user_id_returns_groups():
    groups_expected = [
        {"name": "Grupo A"},
        {"name": "Grupo B"}
    ]
    user_id = '61139221-5e5e-4673-9f9d-7bcc0e2c1eb2'

    response = client.get(f"/groups/{user_id}")
    response_json = response.json()
    response_filtered = [{"name": group["name"]} for group in response_json]

    assert response.status_code == 200
    for group in groups_expected:
        assert group in response_filtered

def test_get_groups_by_user_id_throws_exception_no_groups():
    # user_id no existe
    user_id = '3864dfc4-c9ca-4929-966e-717e7269e69d'

    response = client.get(f"/groups/{user_id}")
    response_json = response.json()

    assert response.status_code == 404
    assert response_json['detail'] == f"No groups found"

def test_get_all_groups_no_groups_found():
    with mock.patch('src.domain.Repository.group_repository.GroupRepository.get_groups',
                    return_value=[]):
        response = client.get("/groups")
        assert response.status_code == 404
        assert response.json()['detail'] == "No groups found"

def test_get_all_groups_generic_exception():
    with mock.patch('src.domain.Repository.group_repository.GroupRepository.get_groups',
                    side_effect=Exception("Unexpected error")):
        response = client.get("/groups")
        assert response.status_code == 500
        assert response.json()['detail'] == "An error occurred while fetching groups"

def test_get_groups_by_user_generic_exception():
    user_id = "61139221-5e5e-4673-9f9d-7bcc0e2c1eb2"
    with mock.patch('src.domain.Repository.group_repository.GroupRepository.get_groups_by_user',
                    side_effect=Exception("Unexpected error")):
        response = client.get(f"/groups/{user_id}")
        assert response.status_code == 500
        assert response.json()['detail'] == "An error occurred while fetching groups"

