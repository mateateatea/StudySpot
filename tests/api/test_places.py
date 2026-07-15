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

    assert "booked_slots" in data["places"][0]

def test_cannot_reserve_already_booked_place():
    payload = {
        "date": "2026-07-15",
        "time_slot": "14:00"
    }

    response = client.post("/reserve/4", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "The slot 2026-07-15 14:00 is already booked"}

def test_can_reserve_free_place():
    payload = {
        "date": "2026-07-16",
        "time_slot": "09:00"
    }

    response = client.post("/reserve/1", json=payload)

    assert response.status_code == 200
    assert "successfully reserved" in response.json()["message"]