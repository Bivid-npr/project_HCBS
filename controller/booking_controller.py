import uuid
import re
from db.connection import get_connection
from models.booking import Booking, Customer, Receipt
from models.enums import BookingStatus, SeatType, ShowTime, UserRole
from models.pricing import PricingPolicy


class BookingController:
    EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    PHONE_RE = re.compile(r"^\+?[0-9][0-9\s().-]{6,19}$")

    def __init__(self):
        self.last_error = ""

    def _validate_customer_details(self, name, phone, email) -> bool:
        self.last_error = ""
        if not name or not phone or not email:
            self.last_error = "Please fill in all customer details."
            return False
        if not self.EMAIL_RE.match(email):
            self.last_error = "Please enter a valid customer email address."
            return False
        digits = re.sub(r"\D", "", phone)
        if not self.PHONE_RE.match(phone) or not (7 <= len(digits) <= 15):
            self.last_error = "Please enter a valid customer phone number."
            return False
        return True

    def _is_actor_authorized_for_cinema(self, actor, cinema_id) -> bool:
        if actor is None:
            return False
        if actor.role in (UserRole.ADMIN, UserRole.MANAGER):
            return True
        return (
            actor.role == UserRole.BOOKING_STAFF
            and getattr(actor, "assigned_cinema_id", None) == cinema_id
        )

    def _is_actor_authorized_for_listing(self, actor, listing_id) -> bool:
        cinema_id = self.get_cinema_id_for_listing(listing_id)
        return cinema_id is not None and self._is_actor_authorized_for_cinema(actor, cinema_id)
    
    def get_pricing_for_cinema(self, cinema_id) -> PricingPolicy:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT pp.policy_id, pp.city_id, pp.morning_price,
                   pp.afternoon_price, pp.evening_price,
                   pp.upper_gallery_multiplier, pp.vip_multiplier
            FROM pricing_policy pp
            JOIN cinema c ON pp.city_id = c.city_id
            WHERE c.cinema_id = %s;
        """, (cinema_id,))      
        row= cur.fetchone()
        cur.close()
        conn.close()
        if row: 
            return PricingPolicy(*row)
        return None
    
    def get_available_seat_count(self, listing_id) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM seat s
            JOIN listing l ON s.screen_id = l.screen_id
            WHERE l.listing_id = %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM booking_seat bs
                  JOIN booking b ON bs.booking_id = b.booking_id
                  WHERE bs.seat_id = s.seat_id
                    AND b.listing_id = l.listing_id
                    AND b.status = 'CONFIRMED'
              );
        """, (listing_id,))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    def check_availability(self, listing_id, seat_type: SeatType) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""SELECT COUNT(*) FROM seat s
                    JOIN listing l ON s.screen_id = l.screen_id
                    WHERE l.listing_id = %s
                    AND s.seat_type = %s
                    AND NOT EXISTS (
                        SELECT 1
                        FROM booking_seat bs
                        JOIN booking b ON bs.booking_id = b.booking_id
                        WHERE bs.seat_id = s.seat_id
                          AND b.listing_id = l.listing_id
                          AND b.status = 'CONFIRMED'
                    );
        """,(listing_id, seat_type.value))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count
    
    def calculate_price(self, cinema_id, show_time_category: ShowTime,
                        seat_type: SeatType, quantity: int) -> float:
        policy = self.get_pricing_for_cinema(cinema_id)
        if not policy:
            return 0.0
        unit_price = policy.get_price_for_seat_type(show_time_category, seat_type)
        return round(unit_price * quantity, 2)

    def get_cinema_id_for_listing(self, listing_id) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.cinema_id FROM listing l
            JOIN screen s ON l.screen_id = s.screen_id
            WHERE l.listing_id = %s;
        """, (listing_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0] if row else None

    def get_screen_number_for_listing(self, listing_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.screen_number
            FROM listing l
            JOIN screen s ON l.screen_id = s.screen_id
            WHERE l.listing_id = %s;
        """, (listing_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0] if row else None

    def get_booking_date_for_reference(self, booking_reference):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT booking_date
            FROM booking
            WHERE booking_reference = %s;
        """, (booking_reference,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0] if row else None

    def _seat_counts_for_capacity(self, capacity):
        lower_count = round(capacity * 0.30)
        vip_count = min(10, max(capacity - lower_count, 0))
        upper_count = max(capacity - lower_count - vip_count, 0)
        return lower_count, upper_count, vip_count

    def _create_missing_screen_seats(self, cur, screen_id, capacity):
        lower_count, upper_count, vip_count = self._seat_counts_for_capacity(capacity)

        for i in range(1, lower_count + 1):
            cur.execute("""
                INSERT INTO seat (screen_id, seat_number, seat_type, status)
                VALUES (%s, %s, 'LOWER_HALL', 'AVAILABLE');
            """, (screen_id, f"L{i:02d}"))

        for i in range(1, upper_count + 1):
            cur.execute("""
                INSERT INTO seat (screen_id, seat_number, seat_type, status)
                VALUES (%s, %s, 'UPPER_GALLERY', 'AVAILABLE');
            """, (screen_id, f"U{i:02d}"))

        for i in range(1, vip_count + 1):
            cur.execute("""
                INSERT INTO seat (screen_id, seat_number, seat_type, status)
                VALUES (%s, %s, 'VIP', 'AVAILABLE');
            """, (screen_id, f"V{i:02d}"))

    def _ensure_listing_seats(self, conn, cur, listing_id):
        cur.execute("""
            SELECT s.screen_id, s.capacity
            FROM listing l
            JOIN screen s ON l.screen_id = s.screen_id
            WHERE l.listing_id = %s
            FOR UPDATE OF s;
        """, (listing_id,))
        row = cur.fetchone()
        if not row:
            return

        screen_id, capacity = row
        cur.execute("SELECT COUNT(*) FROM seat WHERE screen_id = %s;", (screen_id,))
        seat_count = cur.fetchone()[0]
        if seat_count == 0 and capacity > 0:
            self._create_missing_screen_seats(cur, screen_id, capacity)
            conn.commit()

    def get_seats_for_listing(self, listing_id) -> list:
        conn = get_connection()
        cur = conn.cursor()
        self._ensure_listing_seats(conn, cur, listing_id)
        cur.execute("""
            SELECT s.seat_id,
                   s.seat_number,
                   s.seat_type,
                   CASE
                       WHEN EXISTS (
                           SELECT 1
                           FROM booking_seat bs
                           JOIN booking b ON bs.booking_id = b.booking_id
                           WHERE bs.seat_id = s.seat_id
                             AND b.listing_id = l.listing_id
                             AND b.status = 'CONFIRMED'
                       ) THEN 'BOOKED'
                       ELSE 'AVAILABLE'
                   END AS listing_status
            FROM seat s
            JOIN listing l ON s.screen_id = l.screen_id
            WHERE l.listing_id = %s
            ORDER BY s.seat_type, s.seat_number;
        """, (listing_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def calculate_price_for_seat_ids(self, cinema_id, show_time_category,
                                     seat_ids: list) -> float:
        if not seat_ids:
            return 0.0
        policy = self.get_pricing_for_cinema(cinema_id)
        if not policy:
            return 0.0
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT seat_type FROM seat WHERE seat_id = ANY(%s);",
                    (seat_ids,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        from models.enums import SeatType
        total = sum(
            policy.get_price_for_seat_type(show_time_category, SeatType(r[0]))
            for r in rows)
        return round(total, 2)

    def create_booking_with_seats(self, user_id, listing_id, customer_id,
                                   seat_ids: list, cinema_id, show_time_category,
                                   actor=None):
        if not seat_ids:
            return None
        seat_ids = list(dict.fromkeys(seat_ids))
        if not self._is_actor_authorized_for_listing(actor, listing_id):
            print("Unauthorized booking attempt.")
            return None
        actual_cinema_id = self.get_cinema_id_for_listing(listing_id)
        if actual_cinema_id != cinema_id:
            print("Booking cinema does not match listing cinema.")
            return None
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT s.seat_id
                FROM seat s
                JOIN listing l ON s.screen_id = l.screen_id
                WHERE l.listing_id = %s
                  AND s.seat_id = ANY(%s)
                FOR UPDATE OF s;
            """, (listing_id, seat_ids))
            locked_seats = cur.fetchall()
            if len(locked_seats) != len(seat_ids):
                conn.rollback()
                print("One or more selected seats do not belong to this listing.")
                return None
            cur.execute("""
                SELECT COUNT(*)
                FROM booking_seat bs
                JOIN booking b ON bs.booking_id = b.booking_id
                WHERE b.listing_id = %s
                  AND b.status = 'CONFIRMED'
                  AND bs.seat_id = ANY(%s);
            """, (listing_id, seat_ids))
            if cur.fetchone()[0] > 0:
                conn.rollback()
                print("Some seats are no longer available.")
                return None
            total_price = self.calculate_price_for_seat_ids(
                cinema_id, show_time_category, seat_ids)
            booking_ref = "BK-" + str(uuid.uuid4())[:8].upper()
            cur.execute("""
                INSERT INTO booking (booking_reference, customer_id, listing_id,
                                     user_id, total_price, status)
                VALUES (%s, %s, %s, %s, %s, 'CONFIRMED')
                RETURNING booking_id;
            """, (booking_ref, customer_id, listing_id, user_id, total_price))
            booking_id = cur.fetchone()[0]
            for seat_id in seat_ids:
                cur.execute(
                    "INSERT INTO booking_seat (booking_id, seat_id) VALUES (%s, %s);",
                    (booking_id, seat_id))
            cur.execute("INSERT INTO receipt (booking_id) VALUES (%s);", (booking_id,))
            conn.commit()
            print(f"Booking successful! Reference: {booking_ref}")
            return booking_ref
        except Exception as e:
            conn.rollback()
            print("Booking failed.")
            return None
        finally:
            cur.close()
            conn.close()

    def get_cinema_info(self, cinema_id) -> tuple:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.cinema_name, ci.city_name
            FROM cinema c JOIN city ci ON c.city_id = ci.city_id
            WHERE c.cinema_id = %s;
        """, (cinema_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row if row else ("Horizon Cinemas", "")

    def create_booking(self, user_id, listing_id, customer_id,
                       seat_type: SeatType, quantity: int,
                       cinema_id, show_time_category: ShowTime, actor=None):
        if not self._is_actor_authorized_for_listing(actor, listing_id):
            print("Unauthorized booking attempt.")
            return None
        actual_cinema_id = self.get_cinema_id_for_listing(listing_id)
        if actual_cinema_id != cinema_id:
            print("Booking cinema does not match listing cinema.")
            return None
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT s.seat_id FROM seat s
                JOIN screen sc ON s.screen_id = sc.screen_id
                JOIN listing l ON sc.screen_id = l.screen_id
                WHERE l.listing_id = %s
                AND s.seat_type = %s
                AND NOT EXISTS (
                    SELECT 1
                    FROM booking_seat bs
                    JOIN booking b ON bs.booking_id = b.booking_id
                    WHERE bs.seat_id = s.seat_id
                      AND b.listing_id = l.listing_id
                      AND b.status = 'CONFIRMED'
                )
                ORDER BY s.seat_number
                LIMIT %s
                FOR UPDATE OF s;
            """, (listing_id, seat_type.value, quantity))
            seats = cur.fetchall()

            if len(seats) < quantity:
                conn.rollback()
                print("Not enough seats available.")
                return None
            seat_ids = [seat_id for (seat_id,) in seats]
            cur.execute("""
                SELECT COUNT(*)
                FROM booking_seat bs
                JOIN booking b ON bs.booking_id = b.booking_id
                WHERE b.listing_id = %s
                  AND b.status = 'CONFIRMED'
                  AND bs.seat_id = ANY(%s);
            """, (listing_id, seat_ids))
            if cur.fetchone()[0] > 0:
                conn.rollback()
                print("Some seats were booked by another transaction.")
                return None

            total_price = self.calculate_price(
                cinema_id, show_time_category, seat_type, quantity)

            booking_ref = "BK-" + str(uuid.uuid4())[:8].upper()

            cur.execute("""
                INSERT INTO booking (booking_reference, customer_id, listing_id,
                                     user_id, total_price, status)
                VALUES (%s, %s, %s, %s, %s, 'CONFIRMED')
                RETURNING booking_id;
            """, (booking_ref, customer_id, listing_id, user_id, total_price))
            booking_id = cur.fetchone()[0]
            for (seat_id,) in seats:
                cur.execute("""
                    INSERT INTO booking_seat (booking_id, seat_id)
                    VALUES (%s, %s);
                """, (booking_id, seat_id))

            cur.execute("""
                INSERT INTO receipt (booking_id) VALUES (%s);
            """, (booking_id,))

            conn.commit()
            print(f"Booking successful! Reference: {booking_ref}")
            return booking_ref

        except Exception as e:
            conn.rollback()
            print("Booking failed.")
            return None
        finally:
            cur.close()
            conn.close()

    def find_booking(self, booking_reference) -> Booking:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT booking_id, booking_reference, user_id, listing_id,
                   customer_id, total_price, status, booking_date
            FROM booking WHERE booking_reference = %s;
        """, (booking_reference,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return Booking(row[0], row[1], row[2], row[3],
                           row[4], row[5], BookingStatus(row[6]), row[7])
        return None

    def get_customer_or_create(self, name, phone, email) -> int:
        name = name.strip()
        phone = phone.strip()
        email = email.strip().lower()
        if not self._validate_customer_details(name, phone, email):
            return None
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT customer_id FROM customer WHERE email = %s;", (email,))
        row = cur.fetchone()
        if row:
            cur.close()
            conn.close()
            return row[0]
        cur.execute("""
            INSERT INTO customer (name, phone, email)
            VALUES (%s, %s, %s) RETURNING customer_id;
        """, (name, phone, email))
        customer_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return customer_id
