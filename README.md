# Hotel Booking System

This project implements a simplified booking system for Crown Hotels using FastAPI and SQLite.

## Prerequisites


 - Python 3.13+
- `uv` package manager


## Setup
```bash
bash scripts/setup.sh

```

## Running
```bash
bash scripts/run.sh
```

The API will be available at `http://localhost:8000`.

## Testing
```bash
bash scripts/test.sh
```

## API Examples
Register guest:
```bash
curl -X POST http://localhost:8000/guests -H 'Content-Type: application/json' -d '{"name":"Alice","age":30}'
```

Create booking:
```bash
curl -X POST http://localhost:8000/bookings -H 'Content-Type: application/json' \
    -d '{"guest_id":"<guest_id>","room_number":"101","check_in":"2025-01-01","check_out":"2025-01-05"}'
```

Cancel booking:
```bash
curl -X DELETE http://localhost:8000/bookings/<reference>
```

Check available rooms:
```bash
curl "http://localhost:8000/rooms/availability?room_type=standard&check_in=2025-01-01&check_out=2025-01-05"
```
