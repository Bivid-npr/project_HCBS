from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from db.connection import get_connection
from models.enums import BookingStatus, UserRole
from controller.booking_controller import BookingController


class CancellationController:

    CANCELLATION_CHARGE_PERCENT = Decimal("0.50")

    def __init__(self):
        self.last_error = ""

    def _is_actor_authorized_for_listing(self, actor, listing_id) -> bool:
        if actor is None:
            return False
        if actor.role in (UserRole.ADMIN, UserRole.MANAGER):
            return True

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT s.cinema_id
                FROM listing l
                JOIN screen s ON l.screen_id = s.screen_id
                WHERE l.listing_id = %s;
            """, (listing_id,))
            row = cur.fetchone()
            if not row:
                return False
            return (
                actor.role == UserRole.BOOKING_STAFF
                and getattr(actor, "assigned_cinema_id", None) == row[0]
            )
        finally:
            cur.close()
            conn.close()

    def validate_cancellation_date(self, listing_id) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT show_date FROM listing WHERE listing_id = %s;",
                    (listing_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return False
        show_date = row[0]
        return date.today() < show_date
    
    def calculate_refund(self, total_price) -> float:
        amount = Decimal(str(total_price))
        charge = (amount * self.CANCELLATION_CHARGE_PERCENT).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return (amount - charge).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def cancel_booking(self, booking_reference, actor=None) -> bool:
        self.last_error = ""
        booking_ctrl = BookingController()
        booking = booking_ctrl.find_booking(booking_reference)
        
        if not booking:
            self.last_error = "Booking not found. Check the booking reference and try again."
            print(self.last_error)
            return None

        if booking.status == BookingStatus.CANCELLED:
            self.last_error = "This booking has already been cancelled."
            print(self.last_error)
            return None

        if not self._is_actor_authorized_for_listing(actor, booking.listing_id):
            self.last_error = "You are not authorized to cancel this booking."
            print(self.last_error)
            return None

        if not self.validate_cancellation_date(booking.listing_id):
            self.last_error = "Cannot cancel on the day of the show or after."
            print(self.last_error)
            return None

        refund = self.calculate_refund(booking.total_price)

        conn = get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                UPDATE booking SET status = 'CANCELLED'
                WHERE booking_id = %s;
            """, (booking.booking_id,))

            conn.commit()
            print(f"Booking {booking_reference} cancelled. Refund: \u00a3{refund}")
            return refund

        except Exception as e:
            conn.rollback()
            self.last_error = "Cancellation failed. Please try again."
            print("Cancellation failed.")
            return None
        finally:
            cur.close()
            conn.close()
