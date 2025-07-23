from datetime import date, timedelta
from src.domain.entities import Guest, Room
from src.domain.value_objects import RoomType
from src.application.use_cases import CreateBookingUseCase
from src.infrastructure.payment import MockPaymentService
from infrastructure.repositories import (
    SqlAlchemyBookingRepository,
    SqlAlchemyGuestRepository,
    SqlAlchemyRoomRepository,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from infrastructure.models import Base, RoomModel

def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(bind=engine)

def test_create_booking_succeeds():
    session = setup_in_memory_db()

    guest_repo = SqlAlchemyGuestRepository(session)
    room_repo = SqlAlchemyRoomRepository(session)
    booking_repo = SqlAlchemyBookingRepository(session)

    guest = Guest("guest-123", "Test Guest", 25)
    room = Room("001", RoomType.STANDARD)

    guest_repo.add(guest)
    session.add(RoomModel(number=room.number, type=room.room_type.value))  # ✅ ORM insert
    session.commit()

    use_case = CreateBookingUseCase(booking_repo, room_repo, guest_repo, MockPaymentService())

    check_in = date.today() + timedelta(days=2)
    check_out = check_in + timedelta(days=3)

    booking = use_case.execute(guest.id, room.number, check_in, check_out)

    assert booking.guest.id == guest.id
    assert booking.room.number == room.number
    assert booking.status == "booked"
    assert booking.price == 3 * room.room_type.price
