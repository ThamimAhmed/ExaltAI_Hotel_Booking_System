from typing import List, Optional

from sqlalchemy.orm import Session


from domain.entities import Booking, Guest, Room
from domain.value_objects import BookingReference, RoomType
from application.ports import (
    BookingRepositoryPort,
    RoomRepositoryPort,
    GuestRepositoryPort,
)
from .models import BookingModel, GuestModel, RoomModel

class SqlAlchemyBookingRepository(BookingRepositoryPort):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, booking: Booking) -> None:
        model = BookingModel(
            reference=booking.reference.value,
            room_number=booking.room.number,
            guest_id=booking.guest.id,
            check_in=booking.check_in,
            check_out=booking.check_out,
            status=booking.status,
            price=booking.price,
        )
        self.session.add(model)
        self.session.commit()

    def get(self, reference: BookingReference) -> Optional[Booking]:
        m = self.session.get(BookingModel, reference.value)
        if m:
            room = self.session.get(RoomModel, m.room_number)
            guest = self.session.get(GuestModel, m.guest_id)
            booking = Booking(Room(room.number, RoomType(room.type)), Guest(guest.id, guest.name, guest.age), m.check_in, m.check_out, BookingReference(m.reference))
            booking.status = m.status
            booking.price = m.price
            return booking
        return None

    def list(self) -> List[Booking]:
        return [self.get(BookingReference(m.reference)) for m in self.session.query(BookingModel).all()]

    def update(self, booking: Booking) -> None:
        m = self.session.get(BookingModel, booking.reference.value)
        if m:
            m.status = booking.status
            self.session.commit()

class SqlAlchemyRoomRepository(RoomRepositoryPort):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> List[Room]:
        rooms = []
        for m in self.session.query(RoomModel).all():
            rooms.append(Room(m.number, RoomType(m.type)))
        return rooms

    def get(self, number: str) -> Optional[Room]:
        m = self.session.get(RoomModel, number)
        if m:
            return Room(m.number, RoomType(m.type))
        return None

class SqlAlchemyGuestRepository(GuestRepositoryPort):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, guest: Guest) -> None:
        m = GuestModel(id=guest.id, name=guest.name, age=guest.age)
        self.session.add(m)
        self.session.commit()

    def get(self, guest_id: str) -> Optional[Guest]:
        m = self.session.get(GuestModel, guest_id)
        if m:
            return Guest(m.id, m.name, m.age)
        return None

    def list_bookings(self, guest_id: str) -> List[Booking]:

        bookings: List[Booking] = []
        for m in (
            self.session.query(BookingModel)
            .filter_by(guest_id=guest_id)
            .all()
        ):
            room = self.session.get(RoomModel, m.room_number)
            guest = self.session.get(GuestModel, m.guest_id)
            if not room or not guest:
                continue
            booking = Booking(
                Room(room.number, RoomType(room.type)),
                Guest(guest.id, guest.name, guest.age),
                m.check_in,
                m.check_out,
                BookingReference(m.reference),
            )
            booking.status = m.status
            booking.price = m.price
            bookings.append(booking)
        return bookings
