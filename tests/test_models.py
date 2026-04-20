import pytest
from datetime import date
from models.booking import Booking, Customer, Receipt
from models.cinema import Cinema, Screen, Seat, City
from models.film import Film
from models.listing import Listing
from models.pricing import PricingPolicy
from models.user import User, BookingStaff, Admin, Manager
from models.enums import (
    UserRole, SeatType, SeatStatus, BookingStatus, ShowTime
)


class TestCustomer:
    def test_create_customer(self):
        c = Customer(1, "Alice", "07123456789", "alice@email.com")
        assert c.customer_id == 1
        assert c.name == "Alice"
        assert c.phone == "07123456789"
        assert c.email == "alice@email.com"

    def test_get_customer_id(self):
        c = Customer(5, "Bob", "07000000000", "bob@test.com")
        assert c.get_customer_id() == 5

    def test_str_representation(self):
        c = Customer(1, "Alice", "07123456789", "alice@email.com")
        result = str(c)
        assert "Alice" in result
        assert "07123456789" in result
        assert "alice@email.com" in result


class TestBooking:
    def test_create_booking(self):
        b = Booking(1, "BK-ABC12345", 1, 1, 1, 28.80, BookingStatus.CONFIRMED)
        assert b.booking_id == 1
        assert b.booking_reference == "BK-ABC12345"
        assert b.total_price == 28.80
        assert b.status == BookingStatus.CONFIRMED

    def test_get_booking_reference(self):
        b = Booking(1, "BK-XYZ9999", 1, 1, 1, 50.00, BookingStatus.CONFIRMED)
        assert b.get_booking_reference() == "BK-XYZ9999"

    def test_get_status(self):
        b = Booking(1, "BK-TEST", 1, 1, 1, 10.00, BookingStatus.CONFIRMED)
        assert b.get_status() == BookingStatus.CONFIRMED

    def test_get_total_price(self):
        b = Booking(1, "BK-TEST", 1, 1, 1, 45.50, BookingStatus.CONFIRMED)
        assert b.get_total_price() == 45.50

    def test_cancel_changes_status(self):
        b = Booking(1, "BK-CANCEL", 1, 1, 1, 20.00, BookingStatus.CONFIRMED)
        b.cancel()
        assert b.status == BookingStatus.CANCELLED

    def test_cancel_twice_stays_cancelled(self):
        b = Booking(1, "BK-CANCEL2", 1, 1, 1, 20.00, BookingStatus.CONFIRMED)
        b.cancel()
        b.cancel()
        assert b.status == BookingStatus.CANCELLED


class TestReceipt:
    def test_create_receipt(self):
        r = Receipt(1, 1)
        assert r.receipt_id == 1
        assert r.booking_id == 1
        assert r.issue_date is not None

    def test_generate_returns_string(self):
        r = Receipt(1, 1)
        result = r.generate()
        assert "RECEIPT" in result
        assert "Receipt ID" in result
        assert "1" in result
        assert "Booking ID" in result

    def test_print_does_not_raise(self):
        r = Receipt(1, 1)
        try:
            r.print()
        except Exception:
            pytest.fail("print() raised an exception")


class TestSeat:
    def test_create_seat(self):
        s = Seat(1, 1, "L01", SeatType.LOWER_HALL)
        assert s.seat_id == 1
        assert s.seat_number == "L01"
        assert s.seat_type == SeatType.LOWER_HALL
        assert s.status == SeatStatus.AVAILABLE

    def test_is_available_when_available(self):
        s = Seat(1, 1, "L01", SeatType.LOWER_HALL)
        assert s.is_available() is True

    def test_is_available_when_booked(self):
        s = Seat(1, 1, "L01", SeatType.LOWER_HALL, SeatStatus.BOOKED)
        assert s.is_available() is False

    def test_reserve_changes_status(self):
        s = Seat(1, 1, "L01", SeatType.LOWER_HALL)
        s.reserve()
        assert s.status == SeatStatus.RESERVED

    def test_book_changes_status(self):
        s = Seat(1, 1, "L01", SeatType.LOWER_HALL)
        s.book()
        assert s.status == SeatStatus.BOOKED

    def test_release_changes_status(self):
        s = Seat(1, 1, "L01", SeatType.LOWER_HALL, SeatStatus.BOOKED)
        s.release()
        assert s.status == SeatStatus.AVAILABLE


class TestScreen:
    def test_create_screen(self):
        s = Screen(1, 1, 1, 100)
        assert s.screen_id == 1
        assert s.cinema_id == 1
        assert s.screen_number == 1
        assert s.capacity == 100
        assert s.seats == []

    def test_get_available_seats(self):
        s = Screen(1, 1, 1, 10)
        s.seats = [
            Seat(1, 1, "L01", SeatType.LOWER_HALL),
            Seat(2, 1, "L02", SeatType.LOWER_HALL, SeatStatus.BOOKED),
            Seat(3, 1, "L03", SeatType.LOWER_HALL),
        ]
        available = s.get_available_seats()
        assert len(available) == 2

    def test_get_seats_by_type(self):
        s = Screen(1, 1, 1, 10)
        s.seats = [
            Seat(1, 1, "L01", SeatType.LOWER_HALL),
            Seat(2, 1, "U01", SeatType.UPPER_GALLERY),
            Seat(3, 1, "V01", SeatType.VIP),
        ]
        lower = s.get_seats_by_type(SeatType.LOWER_HALL)
        assert len(lower) == 1
        assert lower[0].seat_type == SeatType.LOWER_HALL

    def test_get_seats_by_type_empty(self):
        s = Screen(1, 1, 1, 10)
        s.seats = [Seat(1, 1, "U01", SeatType.UPPER_GALLERY)]
        vip = s.get_seats_by_type(SeatType.VIP)
        assert len(vip) == 0


class TestCinema:
    def test_create_cinema(self):
        c = Cinema(1, "Test Cinema", "City Centre", 1)
        assert c.cinema_id == 1
        assert c.name == "Test Cinema"
        assert c.location == "City Centre"
        assert c.city_id == 1
        assert c.screens == []

    def test_add_screen(self):
        c = Cinema(1, "Test Cinema", "City Centre", 1)
        s = Screen(1, 1, 1, 100)
        c.add_screen(s)
        assert len(c.get_screens()) == 1
        assert c.get_screens()[0].screen_number == 1

    def test_add_multiple_screens(self):
        c = Cinema(1, "Multiplex", "Mall", 1)
        c.add_screen(Screen(1, 1, 1, 100))
        c.add_screen(Screen(2, 1, 2, 80))
        c.add_screen(Screen(3, 1, 3, 60))
        assert len(c.get_screens()) == 3

    def test_get_cinema_id(self):
        c = Cinema(42, "Test", "Test", 1)
        assert c.get_cinema_id() == 42


class TestCity:
    def test_create_city(self):
        c = City(1, "London")
        assert c.city_id == 1
        assert c.name == "London"

    def test_get_city_id(self):
        c = City(5, "Bristol")
        assert c.get_city_id() == 5

    def test_get_city_name(self):
        c = City(3, "Cardiff")
        assert c.get_city_name() == "Cardiff"


class TestFilm:
    def test_create_film(self):
        f = Film(1, "Test Movie", "A test", "Action", "12A", 7.5, 120, "Actor One", 2024)
        assert f.film_id == 1
        assert f.title == "Test Movie"
        assert f.genre == "Action"
        assert f.age_rating == "12A"
        assert f.imdb_rating == 7.5
        assert f.duration == 120
        assert f.cast_members == "Actor One"
        assert f.release_year == 2024

    def test_get_film_id(self):
        f = Film(99, "X", "Y", "Z", "U", 5.0, 90, "A", 2020)
        assert f.get_film_id() == 99

    def test_get_title(self):
        f = Film(1, "Inception", "", "", "", 0, 0, "", 0)
        assert f.get_title() == "Inception"

    def test_str_contains_title_and_year(self):
        f = Film(1, "Jaws", "Shark film", "Thriller", "PG", 8.0, 124, "Roy Scheider", 1975)
        result = str(f)
        assert "Jaws" in result
        assert "1975" in result


class TestListing:
    def test_create_listing(self):
        l = Listing(1, 1, 1, date.today(), "18:00:00", ShowTime.EVENING)
        assert l.listing_id == 1
        assert l.film_id == 1
        assert l.screen_id == 1
        assert l.show_time == "18:00:00"
        assert l.show_time_category == ShowTime.EVENING

    def test_get_listing_id(self):
        l = Listing(7, 2, 3, date.today(), "14:00:00", ShowTime.AFTERNOON)
        assert l.get_listing_id() == 7


class TestPricingPolicy:
    @pytest.fixture
    def london_pricing(self):
        return PricingPolicy(1, 1, 10.00, 11.00, 12.00, 1.20, 1.20)

    def test_create_pricing_policy(self):
        pp = PricingPolicy(1, 1, 10.00, 11.00, 12.00, 1.20, 1.20)
        assert pp.policy_id == 1
        assert pp.city_id == 1
        assert pp.morning_price == 10.00
        assert pp.afternoon_price == 11.00
        assert pp.evening_price == 12.00

    def test_get_base_price_morning(self, london_pricing):
        assert london_pricing.get_base_price(ShowTime.MORNING) == 10.00

    def test_get_base_price_afternoon(self, london_pricing):
        assert london_pricing.get_base_price(ShowTime.AFTERNOON) == 11.00

    def test_get_base_price_evening(self, london_pricing):
        assert london_pricing.get_base_price(ShowTime.EVENING) == 12.00

    def test_lower_hall_price_no_multiplier(self, london_pricing):
        price = london_pricing.get_price_for_seat_type(ShowTime.EVENING, SeatType.LOWER_HALL)
        assert price == 12.00

    def test_upper_gallery_20_percent_more(self, london_pricing):
        price = london_pricing.get_price_for_seat_type(ShowTime.EVENING, SeatType.UPPER_GALLERY)
        assert price == 14.40  # 12 * 1.20

    def test_vip_44_percent_more(self, london_pricing):
        price = london_pricing.get_price_for_seat_type(ShowTime.EVENING, SeatType.VIP)
        assert price == 17.28  # 12 * 1.20 * 1.20 = 17.28

    def test_morning_vip(self, london_pricing):
        price = london_pricing.get_price_for_seat_type(ShowTime.MORNING, SeatType.VIP)
        assert price == 14.40  # 10 * 1.20 * 1.20

    def test_birmingham_pricing(self):
        bham = PricingPolicy(2, 2, 5.00, 6.00, 7.00, 1.20, 1.20)
        assert bham.get_base_price(ShowTime.EVENING) == 7.00
        price = bham.get_price_for_seat_type(ShowTime.AFTERNOON, SeatType.VIP)
        assert price == 8.64  # 6 * 1.20 * 1.20


class TestUserHierarchy:
    def test_booking_staff_role(self):
        u = BookingStaff(1, "staff1", "hash", "John", "john@test.com", 1)
        assert u.role == UserRole.BOOKING_STAFF
        assert u.assigned_cinema_id == 1

    def test_booking_staff_permissions(self):
        u = BookingStaff(1, "staff1", "hash", "John", "john@test.com", 1)
        perms = u.get_permissions()
        assert "view_listing" in perms
        assert "create_booking" in perms
        assert "cancel_booking" in perms
        assert "manage_films" not in perms
        assert "add_cinema" not in perms

    def test_admin_role(self):
        u = Admin(2, "admin1", "hash", "Jane", "jane@test.com")
        assert u.role == UserRole.ADMIN

    def test_admin_permissions(self):
        u = Admin(2, "admin1", "hash", "Jane", "jane@test.com")
        perms = u.get_permissions()
        assert "manage_films" in perms
        assert "manage_listings" in perms
        assert "generate_reports" in perms
        assert "view_all_cinemas" in perms
        assert "add_cinema" not in perms

    def test_manager_role(self):
        u = Manager(3, "manager1", "hash", "Bob", "bob@test.com")
        assert u.role == UserRole.MANAGER

    def test_manager_permissions(self):
        u = Manager(3, "manager1", "hash", "Bob", "bob@test.com")
        perms = u.get_permissions()
        assert "add_cinema" in perms
        assert "manage_cities" in perms
        assert "manage_films" in perms
        assert "generate_reports" in perms

    def test_user_get_id(self):
        u = BookingStaff(42, "staff", "hash", "Name", "email@test.com", 1)
        assert u.get_id() == 42

    def test_user_get_role(self):
        u = Admin(1, "admin", "hash", "Name", "email@test.com")
        assert u.get_role() == UserRole.ADMIN

    def test_user_str(self):
        u = Manager(1, "mgr", "hash", "Alice Manager", "alice@test.com")
        result = str(u)
        assert "Alice Manager" in result
        assert "MANAGER" in result