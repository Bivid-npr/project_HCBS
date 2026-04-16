import pytest
from models.pricing import PricingPolicy
from models.enums import ShowTime, SeatType


class TestPricingPolicy:

    @pytest.fixture
    def london(self):
        return PricingPolicy(1, 1, 10.00, 11.00, 12.00, 1.20, 1.20)

    @pytest.fixture
    def birmingham(self):
        return PricingPolicy(2, 2, 5.00, 6.00, 7.00, 1.20, 1.20)

    # ── Base prices ──────────────────────────────────────────────────────
    def test_base_morning(self, london):
        assert london.get_base_price(ShowTime.MORNING) == 10.00

    def test_base_afternoon(self, london):
        assert london.get_base_price(ShowTime.AFTERNOON) == 11.00

    def test_base_evening(self, london):
        assert london.get_base_price(ShowTime.EVENING) == 12.00

    # ── Lower Hall (no multiplier) ───────────────────────────────────────
    def test_lower_hall_morning(self, london):
        p = london.get_price_for_seat_type(ShowTime.MORNING, SeatType.LOWER_HALL)
        assert p == 10.00

    def test_lower_hall_evening(self, london):
        p = london.get_price_for_seat_type(ShowTime.EVENING, SeatType.LOWER_HALL)
        assert p == 12.00

    # ── Upper Gallery (20% above lower hall) ─────────────────────────────
    def test_upper_gallery_evening(self, london):
        p = london.get_price_for_seat_type(ShowTime.EVENING, SeatType.UPPER_GALLERY)
        assert p == 14.40  # 12.00 * 1.20

    def test_upper_gallery_morning(self, london):
        p = london.get_price_for_seat_type(ShowTime.MORNING, SeatType.UPPER_GALLERY)
        assert p == 12.00  # 10.00 * 1.20

    # ── VIP (20% above upper gallery) ────────────────────────────────────
    def test_vip_evening(self, london):
        p = london.get_price_for_seat_type(ShowTime.EVENING, SeatType.VIP)
        assert p == 17.28  # 12.00 * 1.20 * 1.20

    def test_vip_morning(self, london):
        p = london.get_price_for_seat_type(ShowTime.MORNING, SeatType.VIP)
        assert p == 14.40  # 10.00 * 1.20 * 1.20

    def test_vip_afternoon(self, london):
        p = london.get_price_for_seat_type(ShowTime.AFTERNOON, SeatType.VIP)
        assert p == 15.84  # 11.00 * 1.20 * 1.20

    # ── Birmingham pricing ────────────────────────────────────────────────
    def test_bham_evening_lower(self, birmingham):
        p = birmingham.get_price_for_seat_type(ShowTime.EVENING, SeatType.LOWER_HALL)
        assert p == 7.00

    def test_bham_evening_upper(self, birmingham):
        p = birmingham.get_price_for_seat_type(ShowTime.EVENING, SeatType.UPPER_GALLERY)
        assert p == 8.40  # 7.00 * 1.20

    def test_bham_evening_vip(self, birmingham):
        p = birmingham.get_price_for_seat_type(ShowTime.EVENING, SeatType.VIP)
        assert p == 10.08  # 7.00 * 1.20 * 1.20

    # ── Edge cases ───────────────────────────────────────────────────────
    def test_zero_price(self):
        pp = PricingPolicy(1, 1, 0.00, 0.00, 0.00, 1.20, 1.20)
        p = pp.get_price_for_seat_type(ShowTime.MORNING, SeatType.VIP)
        assert p == 0.00

    def test_different_multipliers(self):
        pp = PricingPolicy(1, 1, 10.00, 10.00, 10.00, 1.50, 1.50)
        upper = pp.get_price_for_seat_type(ShowTime.EVENING, SeatType.UPPER_GALLERY)
        vip = pp.get_price_for_seat_type(ShowTime.EVENING, SeatType.VIP)
        assert upper == 15.00
        assert vip == 22.50


class TestPricingAcrossCities:
    """Verify that different cities can have different base prices."""

    def test_london_vs_birmingham_evening_lower(self):
        london = PricingPolicy(1, 1, 10.00, 11.00, 12.00, 1.20, 1.20)
        bham = PricingPolicy(2, 2, 5.00, 6.00, 7.00, 1.20, 1.20)
        assert london.get_price_for_seat_type(ShowTime.EVENING, SeatType.LOWER_HALL) == 12.00
        assert bham.get_price_for_seat_type(ShowTime.EVENING, SeatType.LOWER_HALL) == 7.00

    def test_london_vs_birmingham_evening_vip(self):
        london = PricingPolicy(1, 1, 10.00, 11.00, 12.00, 1.20, 1.20)
        bham = PricingPolicy(2, 2, 5.00, 6.00, 7.00, 1.20, 1.20)
        assert london.get_price_for_seat_type(ShowTime.EVENING, SeatType.VIP) == 17.28
        assert bham.get_price_for_seat_type(ShowTime.EVENING, SeatType.VIP) == 10.08