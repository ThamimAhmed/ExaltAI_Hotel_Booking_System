from src.application.use_cases import CancelBookingUseCase
from src.domain.entities import Booking, Guest, Room
from src.domain.value_objects import RoomType
from infrastructure.repositories import SqlAlchemyBookingRepository
from infrastructure.models import Base, GuestModel, RoomModel, BookingModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date, timedelta

def test_cancel_booking():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    guest = Guest("g1", "Jane", 25)
    room = Room("101", RoomType.STANDARD)
    check_in = date.today() + timedelta(days=3)
    check_out = check_in + timedelta(days=2)
    booking = Booking(room, guest, check_in, check_out)

    session.add_all([
        GuestModel(id=guest.id, name=guest.name, age=guest.age),
        RoomModel(number=room.number, type=room.room_type.value),
        BookingModel(
            reference=booking.reference.value,
            guest_id=guest.id,
            room_number=room.number,
            check_in=check_in,
            check_out=check_out,
            status="booked",
            price=booking.price
        )
    ])
    session.commit()

    repo = SqlAlchemyBookingRepository(session)
    use_case = CancelBookingUseCase(repo)
    updated = use_case.execute(booking.reference.value)

    assert updated.status == "cancelled"
