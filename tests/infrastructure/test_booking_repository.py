from infrastructure.repositories import SqlAlchemyBookingRepository
from src.domain.entities import Booking, Room, Guest
from src.domain.value_objects import RoomType
from infrastructure.models import Base, GuestModel, RoomModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date, timedelta

def test_add_and_get_booking():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    guest = Guest("g1", "Alice", 28)
    room = Room("101", RoomType.SUITE)
    booking = Booking(
        room=room,
        guest=guest,
        check_in=date.today() + timedelta(days=2),
        check_out=date.today() + timedelta(days=5),
    )

    session.add_all([
        GuestModel(id=guest.id, name=guest.name, age=guest.age),
        RoomModel(number=room.number, type=room.room_type.value)
    ])
    session.commit()

    repo = SqlAlchemyBookingRepository(session)
    repo.add(booking)

    fetched = repo.get(booking.reference)
    assert fetched is not None
    assert fetched.room.number == "101"
    assert fetched.status == "booked"
