from abc import ABC, abstractmethod
from models.enums import UserRole

class User(ABC):
    def __init__(self, user_id, username, password_hash, full_name, email, role: UserRole):
        self.user_id = user_id
        self.username = username
        self.password_hash= password_hash
        self.full_name = full_name
        self.email = email
        self.role = role
        
    @abstractmethod
    def get_permissions(self) ->list:
        pass
    
    def get_id(self) ->int:
        return self.user_id
    
    def get_role(self) ->UserRole:
        return self.role
    
    def __str__(self) ->str:
        return f"{self.full_name} ({self.role.value})"
    
    

class BookingStaff(User):
    def __init__(self, user_id, username, password_hash, full_name, email, assigned_cinema_id):
       super().__init__(user_id, username, password_hash, full_name, email, UserRole.BOOKING_STAFF)
       self.assigned_cinema_id= assigned_cinema_id 
       
    def get_permissions(self) -> list:
        return["view_listing","create_booking","cancel_booking"]
    
    def view_film_listing(self) ->list:
        return[]
    

class Admin(BookingStaff):
    def __init__(self, user_id, username, password_hash, full_name, email):
        super().__init__(user_id, username, password_hash, full_name, email, assigned_cinema_id=None)
        self.role = UserRole.ADMIN
        
    def get_permissions(self) ->list:
        base_permissions = super().get_permissions()
        admin_permissions = ["manage_films", "manage_listings", "generate_reports", "view_all_cinemas"]
        return base_permissions + admin_permissions
    

class Manager(Admin):
    def __init__(self, user_id, username, password_hash, full_name, email):
        super().__init__(user_id, username, password_hash, full_name, email)
        self.role = UserRole.MANAGER
        
    def get_permissions(self) ->list:
        base_permissions = super().get_permissions()
        manager_permissions = ["add_cinema", "manage_cities"]
        return base_permissions + manager_permissions
        