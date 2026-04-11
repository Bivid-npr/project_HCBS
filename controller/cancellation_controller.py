from datetime import date
from db.connection import get_connection
from models.enums import BookingStatus, SeatStatus
from controller.booking_controller import BookingController


class CancellationController:

    CANCELLATION_CHARGE_PERCENT = 0.50

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
        charge = round(total_price * self.CANCELLATION_CHARGE_PERCENT, 2)
        return round(total_price - charge, 2)
    
    def cancel_booking(self, booking_reference) -> bool:
        booking_ctrl = BookingController()
        booking = booking_ctrl.find_booking(booking_reference)
        
        if not booking:
            print("Booking not found.")
            return False

        if booking.status == BookingStatus.CANCELLED:
            print("Booking already cancelled.")
            return False

        if not self.validate_cancellation_date(booking.listing_id):
            print("Cannot cancel on the day of the show or after.")
            return False

        refund = self.calculate_refund(booking.total_price)

        conn = get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT seat_id FROM booking_seat
                WHERE booking_id = %s;
            """, (booking.booking_id,))
            seats = cur.fetchall()

            for (seat_id,) in seats:
                cur.execute("""
                    UPDATE seat SET status = 'AVAILABLE'
                    WHERE seat_id = %s;
                """, (seat_id,))

            cur.execute("""
                UPDATE booking SET status = 'CANCELLED'
                WHERE booking_id = %s;
            """, (booking.booking_id,))

            conn.commit()
            print(f"Booking {booking_reference} cancelled. Refund: \u00a3{refund}")
            return refund

        except Exception as e:
            conn.rollback()
            print("Cancellation failed:", e)
            return None
        finally:
            cur.close()
            conn.close()