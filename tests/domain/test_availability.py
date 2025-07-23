from datetime import date, timedelta

from domain.entities import Booking, Guest, Room
from domain.value_objects import RoomType
from domain.services import RoomAvailabilityService



def test_availability_excludes_booked_room():
    room = Room("201", RoomType.STANDARD)
    guest = Guest("1", "Bob", 30)
    check_in = date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=2)
    booking = Booking(room, guest, check_in, check_out)
    service = RoomAvailabilityService([booking], [room])
    avail = service.available_rooms(RoomType.STANDARD, check_in, check_out)
    assert len(avail) == 0

