import pytest
from app.main import places_db

# Keep a copy of the original "seed" state so every test starts from
# the exact same data, no matter what order tests run in or whether
# a previous test already booked a slot.
_original_state = [place.copy() for place in places_db]
for place, original in zip(_original_state,places_db):
    place["booked_slots"] = list(original["booked_slots"])

@pytest.fixture(autouse=True)
def reset_places_db():
    # Runs automatically before every test.
    # Resets places_db back to its original seed data so tests never
    # leak state into one another (e.g. a reservation made in one test
    # showing up as 'already booked' in the next).
    places_db.clear()
    for place in _original_state:
        places_db.append({**place, "booked_slots": list(place["booked_slots"])})
    yield
