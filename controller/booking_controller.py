import uuid
from db.connection import get_connection
from models.booking import Booking, Customer, Receipt
from models.enums import BookingStatus, SeatType, ShowTime
from models.pricing import PricingPolicy


class BookingController:
    
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
            JOIN screen sc ON s.screen_id = sc.screen_id
            JOIN listing l ON sc.screen_id = l.screen_id
            WHERE l.listing_id = %s AND s.status = 'AVAILABLE';
        """, (listing_id,))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    def check_availability(self, listing_id, seat_type: SeatType) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""SELECT COUNT(*) FROM seat s
                    JOIN screen sc ON s.screen_id =sc.screen_id
                    JOIN listing l ON sc.screen_id =l.screen_id
                    WHERE l.listing_id = %s
                    AND s.seat_type = %s
                    AND s.status = 'AVAILABLE';
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

    def get_seats_for_listing(self, listing_id) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.seat_id, s.seat_number, s.seat_type, s.status
            FROM seat s
            JOIN screen sc ON s.screen_id = sc.screen_id
            JOIN listing l ON sc.screen_id = l.screen_id
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
                                   seat_ids: list, cinema_id, show_time_category):
        if not seat_ids:
            return None
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT COUNT(*) FROM seat
                WHERE seat_id = ANY(%s) AND status = 'AVAILABLE';
            """, (seat_ids,))
            if cur.fetchone()[0] < len(seat_ids):
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
                cur.execute(
                    "UPDATE seat SET status = 'BOOKED' WHERE seat_id = %s;",
                    (seat_id,))
            cur.execute("INSERT INTO receipt (booking_id) VALUES (%s);", (booking_id,))
            conn.commit()
            print(f"Booking successful! Reference: {booking_ref}")
            return booking_ref
        except Exception as e:
            conn.rollback()
            print("Booking failed:", e)
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
                       cinema_id, show_time_category: ShowTime):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT seat_id FROM seat s
                JOIN screen sc ON s.screen_id = sc.screen_id
                JOIN listing l ON sc.screen_id = l.screen_id
                WHERE l.listing_id = %s
                AND s.seat_type = %s
                AND s.status = 'AVAILABLE'
                ORDER BY s.seat_number
                LIMIT %s;
            """, (listing_id, seat_type.value, quantity))
            seats = cur.fetchall()

            if len(seats) < quantity:
                print("Not enough seats available.")
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
                    UPDATE seat SET status = 'BOOKED'
                    WHERE seat_id = %s;
                """, (seat_id,))

            cur.execute("""
                INSERT INTO receipt (booking_id) VALUES (%s);
            """, (booking_id,))

            conn.commit()
            print(f"Booking successful! Reference: {booking_ref}")
            return booking_ref

        except Exception as e:
            conn.rollback()
            print("Booking failed:", e)
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
