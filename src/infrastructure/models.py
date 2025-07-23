from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RoomModel(Base):
    __tablename__ = "rooms"
    number = Column(String, primary_key=True)
    type = Column(String)

class GuestModel(Base):
    __tablename__ = "guests"
    id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)

class BookingModel(Base):
    __tablename__ = "bookings"
    reference = Column(String, primary_key=True)
    room_number = Column(String)
    guest_id = Column(String)
    check_in = Column(Date)
    check_out = Column(Date)
    status = Column(String)
    price = Column(Float)
