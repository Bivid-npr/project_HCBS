from enum import Enum

class UserRole(Enum):
    BOOKING_STAFF = "BOOKING_STAFF"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"

class SeatType(Enum):
    LOWER_HALL = "LOWER_HALL"
    UPPER_GALLERY = "UPPER_GALLERY"
    VIP = "VIP"

class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    BOOKED = "BOOKED"

class BookingStatus(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class ShowTime(Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"
