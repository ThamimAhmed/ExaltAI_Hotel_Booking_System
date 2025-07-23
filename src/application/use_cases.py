from datetime import date


from src.domain.entities import Booking, BookingError
from src.domain.services import RoomAvailabilityService
from src.domain.value_objects import BookingReference, RoomType

from .ports import (
    BookingRepositoryPort,
    RoomRepositoryPort,
    GuestRepositoryPort,
    PaymentServicePort,
)

class CreateBookingUseCase:
    def __init__(
        self,
        booking_repo: BookingRepositoryPort,
        room_repo: RoomRepositoryPort,
        guest_repo: GuestRepositoryPort,
        payment_service: PaymentServicePort,
    ) -> None:
        self.booking_repo = booking_repo
        self.room_repo = room_repo
        self.guest_repo = guest_repo
        self.payment_service = payment_service

    def execute(
        self, guest_id: str, room_number: str, check_in: date, check_out: date
    ) -> Booking:
        guest = self.guest_repo.get(guest_id)
        if not guest:
            raise BookingError("Guest not found")
        room = self.room_repo.get(room_number)
        if not room:
            raise BookingError("Room not found")
        availability = RoomAvailabilityService(
            self.booking_repo.list(), self.room_repo.list()
        )
        if room not in availability.available_rooms(room.room_type, check_in, check_out):
            raise BookingError("Room not available")
        booking = Booking(room, guest, check_in, check_out)
        if not self.payment_service.charge(booking.price):
            raise BookingError("Payment failed")
        self.booking_repo.add(booking)
        return booking

class CancelBookingUseCase:
    def __init__(self, booking_repo: BookingRepositoryPort) -> None:
        self.booking_repo = booking_repo

    def execute(self, reference: str) -> Booking:
        booking = self.booking_repo.get(BookingReference(reference))
        if not booking:
            raise BookingError("Booking not found")
        booking.cancel()
        self.booking_repo.update(booking)
        return booking


class GetBookingUseCase:
    def __init__(self, booking_repo: BookingRepositoryPort) -> None:
        self.booking_repo = booking_repo

    def execute(self, reference: str) -> Booking:
        booking = self.booking_repo.get(BookingReference(reference))
        if not booking:
            raise BookingError("Booking not found")
        return booking


class CheckInUseCase:
    def __init__(self, booking_repo: BookingRepositoryPort) -> None:
        self.booking_repo = booking_repo

    def execute(self, reference: str) -> Booking:
        booking = self.booking_repo.get(BookingReference(reference))
        if not booking:
            raise BookingError("Booking not found")
        booking.check_in_guest()
        self.booking_repo.update(booking)
        return booking


class CheckOutUseCase:
    def __init__(self, booking_repo: BookingRepositoryPort) -> None:
        self.booking_repo = booking_repo

    def execute(self, reference: str) -> Booking:
        booking = self.booking_repo.get(BookingReference(reference))
        if not booking:
            raise BookingError("Booking not found")
        booking.check_out_guest()
        self.booking_repo.update(booking)
        return booking


class ListRoomsUseCase:
    def __init__(self, room_repo: RoomRepositoryPort) -> None:
        self.room_repo = room_repo

    def execute(self):
        return self.room_repo.list()


class CheckAvailabilityUseCase:
    def __init__(self, booking_repo: BookingRepositoryPort, room_repo: RoomRepositoryPort) -> None:
        self.booking_repo = booking_repo
        self.room_repo = room_repo

    def execute(self, room_type: str, check_in: date, check_out: date):
        service = RoomAvailabilityService(self.booking_repo.list(), self.room_repo.list())
        return service.available_rooms(RoomType(room_type), check_in, check_out)


class ListGuestBookingsUseCase:
    def __init__(self, guest_repo: GuestRepositoryPort) -> None:
        self.guest_repo = guest_repo

    def execute(self, guest_id: str):
        return self.guest_repo.list_bookings(guest_id)

