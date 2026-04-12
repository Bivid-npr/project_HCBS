from db.connection import get_connection
from models.film import Film
from models.listing import Listing
from models.enums import ShowTime
from datetime import datetime, timedelta

class FilmController:
    def get_all_films(self) -> list:
        conn=get_connection()
        cur =conn.cursor()
        cur.execute("""SELECT film_id, title, description, genre, age_rating,
                    imdb_rating, duration, cast_members, release_year
                    FROM film ORDER by title;
        """
        )
        rows= cur.fetchall()
        cur.close()
        conn.close()
        return [Film(*row) for row in rows]
    
    def get_all_listings(self) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""SELECT listing_id, film_id, screen_id, show_date,
                    show_time, show_time_category
                    FROM listing ORDER BY show_date, show_time;
        """
        )
        rows= cur.fetchall()
        cur.close()
        conn.close()
        return [Listing(r[0], r[1], r[2],r[3], r[4], ShowTime(r[5]))for r in rows ]
    
    def get_listings_for_cinema(self, cinema_id) -> list:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT l.listing_id, l.film_id, l.screen_id, l.show_date,
                   l.show_time, l.show_time_category
            FROM listing l
            JOIN screen s ON l.screen_id = s.screen_id
            WHERE s.cinema_id = %s
            ORDER BY l.show_date, l.show_time;
        """, (cinema_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Listing(r[0], r[1], r[2], r[3], r[4], ShowTime(r[5])) for r in rows]

    def get_film_by_id(self, film_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""SELECT film_id, title, description, genre, age_rating,
                    imdb_rating, duration, cast_members, release_year
                    FROM film WHERE film_id = %s;""", (film_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return Film(*row) if row else None

    def update_film(self, film_id, title, description, genre, age_rating,
                    imdb_rating, duration, cast_members, release_year) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE film SET title=%s, description=%s, genre=%s,
                        age_rating=%s, imdb_rating=%s, duration=%s,
                        cast_members=%s, release_year=%s
                        WHERE film_id=%s;""",
                        (title, description, genre, age_rating,
                         imdb_rating, duration, cast_members, release_year, film_id))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print("Error updating film:", e)
            return False
        finally:
            cur.close()
            conn.close()

    def add_film(self, title, description, genre, age_rating,
                 imdb_rating, duration, cast_members, release_year) ->bool:
        conn=get_connection()
        cur=conn.cursor()
        
        try:
            cur.execute("""INSERT INTO film (title, description, genre, age_rating,
                        imdb_rating, duration, cast_members, release_year)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
                        
            """,(title, description, genre, age_rating,
                imdb_rating, duration, cast_members, release_year)
            )
            conn.commit()
            return True
        
        except Exception as e:
            conn.rollback()
            print("Error adding film:", e)
            return False
        
        finally:
            cur.close()
            conn.close()
            
    
  
    def remove_film(self, film_id) -> bool:
        conn =get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM film WHERE film_id= %s;", (film_id,))
            conn.commit()
            return True
        
        except Exception as e:
            conn.rollback()
            print("Error removing film:", e)
            return False
        
        finally:
            cur.close()
            conn.close()     
      
          
    def add_listing(self, film_id, screen_id, show_date,
                     show_time, show_time_category: ShowTime) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""INSERT INTO listing(film_id, screen_id, show_date,
                        show_time, show_time_category)
                        VALUES (%s, %s, %s, %s, %s);
            """, (film_id, screen_id, show_date,
                  show_time, show_time_category.value)
            )
            conn.commit()
            return True
        
        except Exception as e:
            conn.rollback()
            print("Error adding lisitng: ", e)
            return False
        
        finally:
            cur.close()
            conn.close()
                    

    def remove_listing(self, listing_id) ->bool:
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM listing WHERE listing_id =%s;", (listing_id,))
            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("Error removing listing: ",e)
            return False

        finally:
            cur.close()
            conn.close()

    def listing_has_bookings(self, listing_id) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM booking
                    WHERE listing_id = %s
                );
            """, (listing_id,))
            return bool(cur.fetchone()[0])
        finally:
            cur.close()
            conn.close()

    def update_listing(self, listing_id, film_id, screen_id, show_date,
                       show_time, show_time_category: ShowTime) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE listing SET film_id=%s, screen_id=%s, show_date=%s,
                        show_time=%s, show_time_category=%s
                        WHERE listing_id=%s;""",
                        (film_id, screen_id, show_date,
                         show_time, show_time_category.value, listing_id))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print("Error updating listing:", e)
            return False
        finally:
            cur.close()
            conn.close()

    def get_listing_conflict(self, screen_id, show_date, show_time,
                             film_duration_minutes, exclude_listing_id=None):
        conn = get_connection()
        cur = conn.cursor()
        try:
            show_time_str = str(show_time)[:8]
            new_start = datetime.combine(
                show_date,
                datetime.strptime(show_time_str, "%H:%M:%S").time()
            )
            new_end = new_start + timedelta(minutes=int(film_duration_minutes))

            query = """
                SELECT l.listing_id, l.show_time, f.duration, f.title
                FROM listing l
                JOIN film f ON l.film_id = f.film_id
                WHERE l.screen_id = %s AND l.show_date = %s
            """
            params = [screen_id, show_date]
            if exclude_listing_id is not None:
                query += " AND l.listing_id <> %s"
                params.append(exclude_listing_id)
            query += " ORDER BY l.show_time"

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            for listing_id, existing_time, existing_duration, title in rows:
                existing_start = datetime.combine(show_date, existing_time)
                existing_end = existing_start + timedelta(minutes=int(existing_duration))
                if new_start < existing_end and existing_start < new_end:
                    return {
                        "listing_id": listing_id,
                        "title": title,
                        "start": existing_start.time().strftime("%H:%M"),
                        "end": existing_end.time().strftime("%H:%M"),
                    }

            return None
        finally:
            cur.close()
            conn.close()

    def is_listing_slot_available(self, screen_id, show_date, show_time,
                                  film_duration_minutes, exclude_listing_id=None) -> bool:
        conflict = self.get_listing_conflict(
            screen_id,
            show_date,
            show_time,
            film_duration_minutes,
            exclude_listing_id,
        )
        return conflict is None
