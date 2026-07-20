from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="StudySpot API", description="Library seat reservation system")

class ReservationRequest(BaseModel):
    date: str
    time_slot: str

places_db = [
    {"id": 1, "name": "Desk to group work A", "type": "desk", "booked_slots": []},
    {"id": 2, "name": "Desk to group work B", "type": "desk", "booked_slots": ["2026-07-14 10:00"]},
    {"id": 3, "name": "Soundproof cabin A", "type": "cabin", "booked_slots": []},
    {"id": 4, "name": "Soundproof cabin B", "type": "cabin", "booked_slots": ["2026-07-15 14:00"]},
]

_seed_places = [
    {**place, "booked_slots": list(place["booked_slots"])} for place in places_db
]

@app.get("/", response_class=FileResponse)
def read_root():
    return "app/index.html"

@app.get("/places")
def get_places():
    return {"places": places_db}

@app.post("/reserve/{place_id}")
def reserve_place(place_id: int, request: ReservationRequest):
    booking_datetime = f"{request.date} {request.time_slot}"

    for place in places_db:
        if place["id"] == place_id:

            if booking_datetime in place["booked_slots"]:
                raise HTTPException(status_code=400, detail=f"The slot {booking_datetime} is already booked")

            place["booked_slots"].append(booking_datetime)
            return {"message": f"You successfully reserved desk number {place_id} for time {booking_datetime}"}
    
    raise HTTPException(status_code=404, detail="Place not found")


@app.post("/reset")
def reset_places():
    # Restores places_db to its original seed data. Used by teh Playwright
    # UI tests so they don't depend on the app being freshly restarted 
    # before every test run.
    places_db.clear()
    for place in _seed_places:
        places_db.append({**place, "booked_slots": list(place["booked_slots"])})
    return {"message": "places_db has been reset to seed data"}