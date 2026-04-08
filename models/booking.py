from datetime import datetime
from models.enums import BookingStatus

class Customer:
    def __init__ (self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        
    def get_customer_id(self) -> int:
        return self.customer_id
    
    def __str__(self) -> str:
        return f"{self.name} | {self.phone} | {self.email}"
    
    
class Booking:
    def __init__(self, booking_id, booking_reference, user_id, listing_id,
                 customer_id, total_price, status: BookingStatus,
                 booking_date: datetime = None):
        
        self.booking_id = booking_id
        self.booking_reference = booking_reference
        self.user_id = user_id
        self.listing_id = listing_id
        self.customer_id = customer_id
        self.total_price = total_price
        self.status = status
        self.booking_date = booking_date or datetime.now()
        
    def get_booking_reference(self) -> str:
        return self.booking_reference

    def get_status(self) -> BookingStatus:
        return self.status

    def get_total_price(self) -> float:
        return self.total_price
    
    def cancel(self):
        self.status = BookingStatus.CANCELLED
    
    
    def __str__(self) -> str:
        return (f"Ref: {self.booking_reference} |"
                f"Listing : {self.listing_id} |"
                f"Total : \u00a3{self.total_price} "
                f"Status: {self.status.value}")


class Receipt:
    def __init__(self, receipt_id, booking_id, issue_date: datetime = None):
        self.receipt_id = receipt_id
        self.booking_id = booking_id      
        self.issue_date= issue_date or datetime.now()
        
    def generate(self) ->str:
        return(f"--- RECEIPT ---\n"
               f"Receipt ID  : {self.receipt_id}\n"
               f"Booking ID  : {self.booking_id}\n"
               f"Issued      : {self.issue_date}\n"
               f"---------------")
        
    def print(self):
        print(self.generate())
        
               
