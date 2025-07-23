from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infrastructure.repositories import SqlAlchemyGuestRepository
from infrastructure.models import Base, RoomModel, GuestModel, BookingModel
from domain.value_objects import RoomType, BookingReference


def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_list_bookings_returns_complete_booking_objects():
    engine = setup_in_memory_db()
    with Session(engine) as session:
        room = RoomModel(number="101", type=RoomType.STANDARD.value)
        guest = GuestModel(id="g1", name="Alice", age=30)
        session.add_all([room, guest])
        session.commit()

        check_in = date.today() + timedelta(days=5)
        check_out = check_in + timedelta(days=2)
        booking_ref = BookingReference("REF123")
        price = 2 * RoomType.STANDARD.price
        booking = BookingModel(
            reference=booking_ref.value,
            room_number="101",
            guest_id="g1",
            check_in=check_in,
            check_out=check_out,
            status="booked",
            price=price,
        )
        session.add(booking)
        session.commit()

        repo = SqlAlchemyGuestRepository(session)
        bookings = repo.list_bookings("g1")

        assert len(bookings) == 1
        b = bookings[0]
        assert b.reference.value == booking_ref.value
        assert b.room.number == "101"
        assert b.guest.id == "g1"
        assert b.status == "booked"
        assert b.price == price
