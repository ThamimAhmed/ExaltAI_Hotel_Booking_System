from dataclasses import dataclass
from enum import Enum
import random
import string

class RoomType(str, Enum):
    STANDARD = "standard"
    DELUXE = "deluxe"
    SUITE = "suite"

    @property
    def price(self) -> int:
        return {self.STANDARD: 100, self.DELUXE: 200, self.SUITE: 300}[self]

    @property
    def capacity(self) -> int:
        return {self.STANDARD: 2, self.DELUXE: 3, self.SUITE: 4}[self]

@dataclass(frozen=True)
class BookingReference:
    value: str

    @staticmethod
    def generate() -> "BookingReference":
        ref = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return BookingReference(ref)
