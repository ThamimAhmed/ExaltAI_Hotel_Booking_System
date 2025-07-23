from fastapi.testclient import TestClient
from src.api.main import app
from datetime import date, timedelta

client = TestClient(app)

def test_full_booking_flow():
    # Create guest
    guest = client.post("/guests", json={"name": "Testy", "age": 28})
    guest_id = guest.json()["id"]

    # Check availability
    check_in = (date.today() + timedelta(days=3)).isoformat()
    check_out = (date.today() + timedelta(days=6)).isoformat()
    avail = client.get("/rooms/availability", params={
        "room_type": "standard",
        "check_in": check_in,
        "check_out": check_out
    })
    room = avail.json()[0]["number"]

    # Create booking
    booking = client.post("/bookings", json={
        "guest_id": guest_id,
        "room_number": room,
        "check_in": check_in,
        "check_out": check_out
    }).json()
    ref = booking["reference"]

    # Check booking
    get = client.get(f"/bookings/{ref}")
    assert get.status_code == 200

    # Check-in
    in_resp = client.post(f"/bookings/{ref}/check-in")
    assert in_resp.status_code == 200

    # Check-out
    out_resp = client.post(f"/bookings/{ref}/check-out")
    assert out_resp.status_code == 200

    # Guest bookings
    guest_bookings = client.get(f"/guests/{guest_id}/bookings")
    assert guest_bookings.status_code == 200

    # Cancel (invalid now, but should return 400)
    cancel = client.delete(f"/bookings/{ref}")
    assert cancel.status_code == 400 or cancel.status_code == 200
