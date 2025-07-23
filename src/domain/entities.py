from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from .value_objects import RoomType, BookingReference

class BookingError(Exception):
    pass

@dataclass
class Room:
    number: str
    room_type: RoomType

@dataclass
class Guest:
    id: str
    name: str
    age: int

@dataclass
class Booking:
    room: Room
    guest: Guest
    check_in: date
    check_out: date
    reference: BookingReference = field(default_factory=BookingReference.generate)
    status: str = "booked"
    price: int = 0

    def __post_init__(self) -> None:
        if self.guest.age < 18:
            raise BookingError("Guest must be at least 18")
        if self.check_in <= date.today() + timedelta(hours=24):
            raise BookingError("Bookings must be made 24h in advance")
        nights = (self.check_out - self.check_in).days
        if nights <= 0:
            raise BookingError("Invalid stay length")
        if nights > 30:
            raise BookingError("Stay cannot exceed 30 nights")
        self.price = nights * self.room.room_type.price

    def cancel(self, today: Optional[date] = None) -> None:
        today = today or date.today()
        if (self.check_in - today).days < 2:
            raise BookingError("Cannot cancel within 48 hours")
        self.status = "cancelled"

    def check_in_guest(self) -> None:
        if self.status != "booked":
            raise BookingError("Cannot check-in")
        self.status = "checked_in"

    def check_out_guest(self) -> None:
        if self.status != "checked_in":
            raise BookingError("Cannot check-out")
        self.status = "checked_out"
