from models.enums import SeatType, SeatStatus

class Seat:
    def __init__(self, seat_id, screen_id, seat_number, seat_type: SeatType, status: SeatStatus =SeatStatus.AVAILABLE):
        self.seat_id = seat_id
        self.screen_id = screen_id
        self.seat_number= seat_number
        self.seat_type= seat_type
        self.status = status
        
    def is_available(self) -> bool:
        return self.status == SeatStatus.AVAILABLE
    
    def reserve(self):
        self.status = SeatStatus.RESERVED
        
    def book(self):
        self.status = SeatStatus.BOOKED
        
    def release(self):
        self.status= SeatStatus.AVAILABLE
        


class Screen:
    def __init__(self, screen_id, cinema_id, screen_number, capacity):
        self.screen_id= screen_id
        self.cinema_id= cinema_id
        self.screen_number= screen_number
        self.capacity= capacity
        self.seats= []
        
    def get_available_seats(self) -> list:
        return[s for s in self.seats if s.is_available()]
    
    def get_seats_by_type(self, seat_type :SeatType) ->list:
        return [s for s in self.seats if s.seat_type == seat_type]
    
    

class Cinema:
    def __init__(self, cinema_id, name, location, city_id):
        self.cinema_id= cinema_id
        self.name = name
        self.location= location
        self.city_id= city_id
        self.screens=[]
        
    def add_screen(self, screen: Screen):
        self.screens.append(screen)
        
    def get_screens(self) -> list:
        return self.screens
    
    def get_cinema_id(self) -> int:
        return self.cinema_id
    
class City:
    def __init__(self, city_id, name):
        self.city_id = city_id
        self.name = name
            
    def get_city_id(self) -> int:
        return self.city_id
        
    def get_city_name(self,) -> str:
        return self.name
        