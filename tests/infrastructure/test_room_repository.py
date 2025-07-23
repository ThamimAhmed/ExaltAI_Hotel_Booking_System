from infrastructure.repositories import SqlAlchemyRoomRepository
from infrastructure.models import Base, RoomModel
from src.domain.value_objects import RoomType
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

def test_get_room_by_number():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    session.add(RoomModel(number="001", type=RoomType.DELUXE.value))
    session.commit()

    repo = SqlAlchemyRoomRepository(session)
    room = repo.get("001")

    assert room is not None
    assert room.room_type == RoomType.DELUXE
