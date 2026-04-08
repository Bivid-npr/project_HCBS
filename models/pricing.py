from models.enums import SeatType, ShowTime

class PricingPolicy:
    def __init__(self,policy_id, city_id, morning_price, afternoon_price, evening_price, vip_multiplier=1.2, upper_gallery_multiplier=1.2):
        self.policy_id= policy_id
        self.city_id= city_id
        self.morning_price= morning_price
        self.afternoon_price= afternoon_price
        self.evening_price= evening_price
        self.vip_multiplier= vip_multiplier   
        self.upper_gallery_multiplier = upper_gallery_multiplier 
        
    
    def get_base_price(self, show_time: ShowTime) ->float:
        if show_time == ShowTime.MORNING:
            return self.morning_price
        elif show_time == ShowTime.AFTERNOON:
            return self.afternoon_price
        else:
            return self.evening_price
        
    
    def get_price_for_seat_type(self, show_time: ShowTime, seat_type: SeatType) ->float:
        base = self.get_base_price(show_time)
        if seat_type == SeatType.LOWER_HALL:
            return base
        elif seat_type == SeatType.UPPER_GALLERY:
            return round(base * self.upper_gallery_multiplier, 2)
        else:
            upper_price= base * self.upper_gallery_multiplier
            return round(upper_price * self.vip_multiplier, 2)
            