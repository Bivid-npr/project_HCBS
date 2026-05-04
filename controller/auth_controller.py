import hashlib
from db.connection import get_connection
from models.user import BookingStaff, Admin, Manager
from models.enums import UserRole

class AuthController:

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str):
        hashed = self.hash_password(password)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, username, password_hash, full_name,
                   email, role, assigned_cinema_id
            FROM users WHERE username = %s AND password_hash = %s;
        """, (username, hashed))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None

        user_id, username, pwd, full_name, email, role, cinema_id = row

        if role == UserRole.BOOKING_STAFF.value:
            return BookingStaff(user_id, username, pwd, full_name, email, cinema_id)
        elif role == UserRole.ADMIN.value:
            return Admin(user_id, username, pwd, full_name, email)
        elif role == UserRole.MANAGER.value:
            return Manager(user_id, username, pwd, full_name, email)
        return None

    def register_booking_staff(self, username: str, password: str, full_name: str,
                               email: str, assigned_cinema_id: int):
        return self.register_user(
            username,
            password,
            full_name,
            email,
            UserRole.BOOKING_STAFF.value,
            assigned_cinema_id,
        )

    def register_user(self, username: str, password: str, full_name: str,
                      email: str, role: str, assigned_cinema_id=None):
        if role not in [UserRole.BOOKING_STAFF.value, UserRole.ADMIN.value]:
            return False, "Only BOOKING_STAFF and ADMIN users can be registered here."
        if role == UserRole.BOOKING_STAFF.value and assigned_cinema_id is None:
            return False, "Booking staff must be assigned to a cinema."
        if role == UserRole.ADMIN.value:
            assigned_cinema_id = None

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
            if cur.fetchone():
                return False, "Username already exists."

            cur.execute("""
                INSERT INTO users
                    (username, password_hash, full_name, email, role, assigned_cinema_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING user_id;
            """, (
                username,
                self.hash_password(password),
                full_name,
                email,
                role,
                assigned_cinema_id,
            ))
            user_id = cur.fetchone()[0]
            conn.commit()
            return True, user_id
        except Exception as e:
            conn.rollback()
            print("User registration failed.")
            return False, "Registration failed. Please check the details and try again."
        finally:
            cur.close()
            conn.close()

    def get_booking_staff(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, username, full_name, email, assigned_cinema_id
            FROM users
            WHERE role = %s
            ORDER BY full_name, username;
        """, (UserRole.BOOKING_STAFF.value,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def get_users_by_roles(self, roles):
        if not roles:
            return []
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, username, full_name, email, role, assigned_cinema_id
            FROM users
            WHERE role::text = ANY(%s)
            ORDER BY role, full_name, username;
        """, (roles,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
