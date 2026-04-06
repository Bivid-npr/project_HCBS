from models.enums import ShowTime


class Listing:
    def __init__(self, listing_id, film_id, screen_id, show_date, 
                 show_time, show_time_category: ShowTime):
        self.listing_id = listing_id
        self.film_id = film_id
        self.screen_id = screen_id
        self.show_date = show_date
        self.show_time = show_time
        self.show_time_category = show_time_category

    def get_listing_id(self) -> int:
        return self.listing_id

    def __str__(self) -> str:
        return (f"Listing {self.listing_id} | Screen {self.screen_id} | "
                f"{self.show_date} | {self.show_time} | {self.show_time_category.value}")