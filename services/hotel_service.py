from models.room import Room
from models.customer_booking import CustomerBooking

class HotelService:
    def __init__(self, db):
        self.room = Room(db)
        self.cb = CustomerBooking(db)