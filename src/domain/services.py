from datetime import date
from typing import List

from .entities import Room, Booking
from .value_objects import RoomType

class RoomAvailabilityService:
    def __init__(self, bookings: List[Booking], rooms: List[Room]):
        self.bookings = bookings
        self.rooms = rooms

    def available_rooms(self, room_type: RoomType, check_in: date, check_out: date) -> List[Room]:
        booked_numbers = {
            b.room.number
            for b in self.bookings
            if not (b.check_out <= check_in or b.check_in >= check_out)
            and b.status in {"booked", "checked_in"}
        }
        return [r for r in self.rooms if r.room_type == room_type and r.number not in booked_numbers]
