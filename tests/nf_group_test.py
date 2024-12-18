from fastapi.testclient import TestClient
from src.api.main import app
import time

client = TestClient(app)

def test_get_all_groups_less_than_one_sec():
    max_response_time = 1

    start_time = time.perf_counter()
    response = client.get("/groups")
    end_time = time.perf_counter()
    response_time = end_time - start_time

    assert response.status_code == 200
    assert response_time <= max_response_time
