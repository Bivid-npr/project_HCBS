from db.connection import get_connection
from models.cinema import Cinema, Screen, City
from models.pricing import PricingPolicy

class CinemaController:

    def get_all_cinemas(self) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT cinema_id, cinema_name, location, city_id
            FROM cinema ORDER BY city_id, cinema_name;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Cinema(r[0], r[1], r[2], r[3]) for r in rows]

    def get_all_cities(self) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT city_id, city_name FROM city ORDER BY city_name;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [City(r[0], r[1]) for r in rows]

    def get_all_cities_with_pricing(self) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.city_id,
                   c.city_name,
                   pp.morning_price,
                   pp.afternoon_price,
                   pp.evening_price,
                   pp.upper_gallery_multiplier,
                   pp.vip_multiplier
            FROM city c
            LEFT JOIN pricing_policy pp ON c.city_id = pp.city_id
            ORDER BY c.city_name;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def get_screens_for_cinema(self, cinema_id) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT screen_id, cinema_id, screen_number, capacity
            FROM screen WHERE cinema_id = %s
            ORDER BY screen_number;
        """, (cinema_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Screen(r[0], r[1], r[2], r[3]) for r in rows]

    def get_next_screen_number_for_cinema(self, cinema_id) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(MAX(screen_number), 0)
            FROM screen
            WHERE cinema_id = %s;
        """, (cinema_id,))
        next_screen_number = cur.fetchone()[0] + 1
        cur.close()
        conn.close()
        return next_screen_number

    def add_cinema(self, name, location, city_id) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO cinema (cinema_name, location, city_id)
                VALUES (%s, %s, %s);
            """, (name, location, city_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Error adding cinema.")
            return False
        finally:
            cur.close()
            conn.close()

    def add_city(self, city_name) -> int:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO city (city_name) VALUES (%s)
                RETURNING city_id;
            """, (city_name,))
            city_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return city_id
        except Exception as e:
            conn.rollback()
            print("Error adding city.")
            cur.close()
            conn.close()
            return None

    def configure_screens(self, cinema_id, screen_count, capacity) -> list:
        conn = get_connection()
        cur = conn.cursor()
        try:
            created_screen_ids = []
            next_screen_number = self.get_next_screen_number_for_cinema(cinema_id)

            for offset in range(screen_count):
                screen_number = next_screen_number + offset
                cur.execute("""
                    INSERT INTO screen (cinema_id, screen_number, capacity)
                    VALUES (%s, %s, %s)
                    RETURNING screen_id;
                """, (cinema_id, screen_number, capacity))
                screen_id = cur.fetchone()[0]
                created_screen_ids.append(screen_id)

                lower_count = round(capacity * 0.30)
                upper_count = capacity - lower_count - 10
                vip_count = 10

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

            conn.commit()
            return created_screen_ids
        except Exception as e:
            conn.rollback()
            print("Error configuring screen.")
            return []
        finally:
            cur.close()
            conn.close()

    def configure_existing_screen(self, cinema_id, screen_number, capacity) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE screen
                SET capacity = %s
                WHERE cinema_id = %s AND screen_number = %s;
            """, (capacity, cinema_id, screen_number))
            updated = cur.rowcount > 0
            conn.commit()
            return updated
        except Exception as e:
            conn.rollback()
            print("Error configuring existing screen.")
            return False
        finally:
            cur.close()
            conn.close()

    def configure_screen(self, cinema_id, screen_number, capacity) -> bool:
        created = self.configure_screens(cinema_id, 1, capacity)
        return bool(created)

    def set_city_pricing(self, city_id, morning_price, afternoon_price,
                         evening_price, upper_multiplier=1.20,
                         vip_multiplier=1.20) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO pricing_policy
                    (city_id, morning_price, afternoon_price, evening_price,
                     upper_gallery_multiplier, vip_multiplier)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (city_id) DO UPDATE SET
                    morning_price = EXCLUDED.morning_price,
                    afternoon_price = EXCLUDED.afternoon_price,
                    evening_price = EXCLUDED.evening_price,
                    upper_gallery_multiplier = EXCLUDED.upper_gallery_multiplier,
                    vip_multiplier = EXCLUDED.vip_multiplier;
            """, (city_id, morning_price, afternoon_price, evening_price,
                  upper_multiplier, vip_multiplier))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Error setting pricing.")
            return False
        finally:
            cur.close()
            conn.close()
