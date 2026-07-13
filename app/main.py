from fastapi import FastAPI, HTTPException

app = FastAPI(title="StudySpot API", description="Libary seat reservation system")

@app.get("/")
def read_root():
    return {"message": "Welcome to StudySpot! Reservation system is working"}

places_db = [
    {"id": 1, "name": "Desk to group work A", "type": "desk", "is_available": True},
    {"id": 2, "name": "Desk to group work B", "type": "desk", "is_available": True},
    {"id": 3, "name": "Soundproof cabin A", "type": "cabin", "is_available": True},
    {"id": 4, "name": "Soundproof cabin A", "type": "cabin", "is_available": False},
]

@app.get("/places")
def get_places():
    return {"places": places_db}

@app.post("/reserve/{place_id}")
def reserve_place(place_id: int):
    for place in places_db:
        if place["id"] == place_id:
            if not place["is_available"]:
                raise HTTPException(status_code=400, detail="Place is already booked!")
            place["is_available"] = False
            return {"Message": f"Successfully reserved place {place_id}"}
        
    raise HTTPException(status_code=404, detail="Place not found")
