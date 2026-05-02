import sqlite3
from datetime import datetime

# ---------------- DATABASE CONNECTION ----------------
class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect("hotel.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_type TEXT,
            price REAL,
            is_available INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER,
            customer_id INTEGER,
            check_in TEXT,
            check_out TEXT,
            total_amount REAL,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        """)
        self.conn.commit()

    def commit(self):
        self.conn.commit()


# ---------------- ROOM CLASS ----------------
class Room:
    def __init__(self, db):
        self.db = db

    def add_room(self, room_type, price):
        self.db.cursor.execute(
            "INSERT INTO rooms (room_type, price, is_available) VALUES (?, ?, ?)",
            (room_type, price, 1)
        )
        self.db.commit()
        print("Room added successfully")

    def view_available_rooms(self):
        self.db.cursor.execute("SELECT * FROM rooms WHERE is_available=1")
        rooms = self.db.cursor.fetchall()
        for room in rooms:
            print(room)


# ---------------- CUSTOMER CLASS ----------------
class Customer:
    def __init__(self, db):
        self.db = db

    def add_customer(self, name, phone):
        self.db.cursor.execute(
            "INSERT INTO customers (name, phone) VALUES (?, ?)",
            (name, phone)
        )
        self.db.commit()
        print("Customer added successfully")


# ---------------- BOOKING CLASS ----------------
class Booking:
    def __init__(self, db):
        self.db = db

    def book_room(self, room_id, customer_id, check_in, check_out):
        d1 = datetime.strptime(check_in, "%Y-%m-%d")
        d2 = datetime.strptime(check_out, "%Y-%m-%d")
        days = (d2 - d1).days

        self.db.cursor.execute("SELECT price FROM rooms WHERE room_id=?", (room_id,))
        result = self.db.cursor.fetchone()

        if result is None:
            print("Invalid room ID")
            return

        price = result[0]
        total = price * days

        self.db.cursor.execute("""
            INSERT INTO bookings (room_id, customer_id, check_in, check_out, total_amount)
            VALUES (?, ?, ?, ?, ?)
        """, (room_id, customer_id, check_in, check_out, total))

        self.db.cursor.execute(
            "UPDATE rooms SET is_available=0 WHERE room_id=?", (room_id,)
        )

        self.db.commit()
        print("Room booked successfully. Total:", total)

    def cancel_booking(self, booking_id):
        self.db.cursor.execute(
            "SELECT room_id FROM bookings WHERE booking_id=?", (booking_id,)
        )
        result = self.db.cursor.fetchone()

        if result is None:
            print("Invalid booking ID")
            return

        room_id = result[0]

        self.db.cursor.execute(
            "DELETE FROM bookings WHERE booking_id=?", (booking_id,)
        )

        self.db.cursor.execute(
            "UPDATE rooms SET is_available=1 WHERE room_id=?", (room_id,)
        )

        self.db.commit()
        print("Booking cancelled")

    def generate_bill(self, booking_id):
        self.db.cursor.execute(
            "SELECT * FROM bookings WHERE booking_id=?", (booking_id,)
        )
        bill = self.db.cursor.fetchone()

        if bill:
            print("Bill Details:", bill)
        else:
            print("Invalid booking ID")


# ---------------- MAIN MENU ----------------
def main():
    db = DBConnection()
    room = Room(db)
    customer = Customer(db)
    booking = Booking(db)

    while True:
        print("\n--- HOTEL MANAGEMENT SYSTEM ---")
        print("1. Add Room")
        print("2. View Available Rooms")
        print("3. Add Customer")
        print("4. Book Room")
        print("5. Cancel Booking")
        print("6. Generate Bill")
        print("7. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            rt = input("Room Type: ")
            price = float(input("Price: "))
            room.add_room(rt, price)

        elif choice == 2:
            room.view_available_rooms()

        elif choice == 3:
            name = input("Name: ")
            phone = input("Phone: ")
            customer.add_customer(name, phone)

        elif choice == 4:
            rid = int(input("Room ID: "))
            cid = int(input("Customer ID: "))
            cin = input("Check-in (YYYY-MM-DD): ")
            cout = input("Check-out (YYYY-MM-DD): ")
            booking.book_room(rid, cid, cin, cout)

        elif choice == 5:
            bid = int(input("Booking ID: "))
            booking.cancel_booking(bid)

        elif choice == 6:
            bid = int(input("Booking ID: "))
            booking.generate_bill(bid)

        elif choice == 7:
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()