from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import uuid



from src.domain.entities import BookingError, Guest
from src.application.use_cases import (

    CreateBookingUseCase,
    CancelBookingUseCase,
    GetBookingUseCase,
    CheckInUseCase,
    CheckOutUseCase,
    ListRoomsUseCase,
    CheckAvailabilityUseCase,
    ListGuestBookingsUseCase,
)
from infrastructure.models import Base
from infrastructure.repositories import (

    SqlAlchemyBookingRepository,
    SqlAlchemyGuestRepository,
    SqlAlchemyRoomRepository,
)


from src.infrastructure.payment import MockPaymentService

engine = create_engine("sqlite:///hotel.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

app = FastAPI()


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


class BookingRequest(BaseModel):
    guest_id: str
    room_number: str
    check_in: date
    check_out: date

class BookingResponse(BaseModel):
    reference: str
    status: str
    price: int

class GuestRequest(BaseModel):
    name: str
    age: int


@app.post("/guests")
def register_guest(payload: GuestRequest):
    with Session(engine) as session:
        repo = SqlAlchemyGuestRepository(session)
        guest = Guest(str(uuid.uuid4()), payload.name, payload.age)
        repo.add(guest)
        return {"id": guest.id}


@app.post("/bookings", response_model=BookingResponse)
def create_booking(payload: BookingRequest):
    with Session(engine) as session:
        booking_repo = SqlAlchemyBookingRepository(session)
        room_repo = SqlAlchemyRoomRepository(session)
        guest_repo = SqlAlchemyGuestRepository(session)
        use_case = CreateBookingUseCase(
            booking_repo, room_repo, guest_repo, MockPaymentService()
        )
        try:
            booking = use_case.execute(
                payload.guest_id,
                payload.room_number,
                payload.check_in,
                payload.check_out,
            )
        except BookingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return BookingResponse(
            reference=booking.reference.value, status=booking.status, price=booking.price
        )


@app.delete("/bookings/{reference}", response_model=BookingResponse)
def cancel_booking(reference: str):
    with Session(engine) as session:
        booking_repo = SqlAlchemyBookingRepository(session)
        use_case = CancelBookingUseCase(booking_repo)
        try:
            booking = use_case.execute(reference)
        except BookingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return BookingResponse(reference=booking.reference.value, status=booking.status, price=booking.price)


@app.get("/bookings/{reference}", response_model=BookingResponse)
def get_booking(reference: str):
    with Session(engine) as session:
        booking_repo = SqlAlchemyBookingRepository(session)
        use_case = GetBookingUseCase(booking_repo)
        try:
            booking = use_case.execute(reference)
        except BookingError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return BookingResponse(reference=booking.reference.value, status=booking.status, price=booking.price)


@app.post("/bookings/{reference}/check-in", response_model=BookingResponse)
def check_in(reference: str):
    with Session(engine) as session:
        booking_repo = SqlAlchemyBookingRepository(session)
        use_case = CheckInUseCase(booking_repo)
        try:
            booking = use_case.execute(reference)
        except BookingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return BookingResponse(reference=booking.reference.value, status=booking.status, price=booking.price)


@app.post("/bookings/{reference}/check-out", response_model=BookingResponse)
def check_out(reference: str):
    with Session(engine) as session:
        booking_repo = SqlAlchemyBookingRepository(session)
        use_case = CheckOutUseCase(booking_repo)
        try:
            booking = use_case.execute(reference)
        except BookingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return BookingResponse(reference=booking.reference.value, status=booking.status, price=booking.price)


@app.get("/rooms")
def list_rooms():
    with Session(engine) as session:
        room_repo = SqlAlchemyRoomRepository(session)
        use_case = ListRoomsUseCase(room_repo)
        rooms = use_case.execute()
        return [{"number": r.number, "type": r.room_type.value} for r in rooms]


@app.get("/rooms/availability")
def check_availability(room_type: str, check_in: date, check_out: date):
    with Session(engine) as session:
        booking_repo = SqlAlchemyBookingRepository(session)
        room_repo = SqlAlchemyRoomRepository(session)
        use_case = CheckAvailabilityUseCase(booking_repo, room_repo)
        rooms = use_case.execute(room_type, check_in, check_out)
        return [{"number": r.number, "type": r.room_type.value} for r in rooms]


@app.get("/guests/{guest_id}/bookings")
def guest_bookings(guest_id: str):
    with Session(engine) as session:
        guest_repo = SqlAlchemyGuestRepository(session)
        use_case = ListGuestBookingsUseCase(guest_repo)
        bookings = use_case.execute(guest_id)
        return [
            {
                "reference": b.reference.value,
                "room_number": b.room.number,
                "status": b.status,
            }
            for b in bookings
        ]

