from datetime import date, timedelta

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))


from domain.entities import Booking, Guest, Room, BookingError
from domain.value_objects import RoomType



def test_booking_price_and_reference():
    room = Room("101", RoomType.STANDARD)
    guest = Guest("1", "Bob", 30)
    check_in = date.today() + timedelta(days=2)
    check_out = check_in + timedelta(days=2)
    booking = Booking(room, guest, check_in, check_out)
    assert booking.price == 2 * RoomType.STANDARD.price
    assert len(booking.reference.value) == 10


def test_underage_guest():
    room = Room("101", RoomType.STANDARD)
    guest = Guest("1", "Bob", 17)
    check_in = date.today() + timedelta(days=2)
    check_out = check_in + timedelta(days=2)
    try:
        Booking(room, guest, check_in, check_out)
    except BookingError:
        assert True
    else:
        assert False



def test_cancel_and_flow():
    room = Room("102", RoomType.STANDARD)
    guest = Guest("2", "Alice", 25)
    check_in = date.today() + timedelta(days=3)
    check_out = check_in + timedelta(days=2)
    booking = Booking(room, guest, check_in, check_out)
    booking.check_in_guest()
    booking.check_out_guest()
    assert booking.status == "checked_out"
    booking = Booking(room, guest, check_in, check_out)
    booking.cancel(today=check_in - timedelta(days=3))
    assert booking.status == "cancelled"

