from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {"message": "Welcome to StudySpot! Reservation system is working"}

def test_get_places():
    response = client.get("/places")

    assert response.status_code == 200

    data = response.json()

    assert "places" in data

    assert len(data["places"]) == 4

def test_cannot_reserve_already_booked_place():
    response = client.post("/reserve/4")

    assert response.status_code == 400