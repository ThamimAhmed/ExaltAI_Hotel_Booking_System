from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional


from src.domain.entities import Booking, Guest, Room
from src.domain.value_objects import BookingReference


class BookingRepositoryPort(ABC):
    @abstractmethod
    def add(self, booking: Booking) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: BookingReference) -> Optional[Booking]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Booking]:
        raise NotImplementedError

    @abstractmethod
    def update(self, booking: Booking) -> None:
        raise NotImplementedError

class RoomRepositoryPort(ABC):
    @abstractmethod
    def list(self) -> List[Room]:
        raise NotImplementedError

    @abstractmethod
    def get(self, number: str) -> Optional[Room]:
        raise NotImplementedError

class GuestRepositoryPort(ABC):
    @abstractmethod
    def add(self, guest: Guest) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, guest_id: str) -> Optional[Guest]:
        raise NotImplementedError

    @abstractmethod
    def list_bookings(self, guest_id: str) -> List[Booking]:
        raise NotImplementedError

class PaymentServicePort(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        raise NotImplementedError
