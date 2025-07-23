#!/bin/bash
set -e
PYTHON_BIN="python3.13"
if ! command -v $PYTHON_BIN >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi
uv venv --python="$PYTHON_BIN" .venv

source .venv/Scripts/activate
uv pip install --upgrade pip
uv pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite pydantic pytest \
pytest-cov ruff pyre-check

python - <<'PY'
from pathlib import Path
from sqlalchemy import create_engine, Column, String, Integer, Date, Enum, Float
from sqlalchemy.orm import declarative_base, Session
Base = declarative_base()
class Room(Base):
    __tablename__ = 'rooms'
    number = Column(String, primary_key=True)
    type = Column(String)
class Guest(Base):
    __tablename__ = 'guests'
    id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)
class Booking(Base):
    __tablename__ = 'bookings'
    reference = Column(String, primary_key=True)
    room_number = Column(String)
    guest_id = Column(String)
    check_in = Column(Date)
    check_out = Column(Date)
    status = Column(String)
    price = Column(Float)
engine = create_engine('sqlite:///hotel.db')
Base.metadata.create_all(engine)
with Session(engine) as session:
    if not session.query(Room).first():
        for i in range(1, 51):
            session.add(Room(number=f"{i:03}", type="standard"))
        for i in range(51, 91):
            session.add(Room(number=f"{i:03}", type="deluxe"))
        for i in range(91, 101):
            session.add(Room(number=f"{i:03}", type="suite"))
        session.commit()
PY
mkdir -p src/domain src/application src/infrastructure src/api tests scripts
chmod +x scripts/run.sh scripts/test.sh scripts/setup.sh
