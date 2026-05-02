from datetime import datetime

class CustomerBooking:
    def __init__(self, db):
        self.db = db

    # -------- CUSTOMER --------
    def add_customer(self, name, phone):
        query = "INSERT INTO customers (name, phone) VALUES (%s, %s)"
        self.db.cursor.execute(query, (name, phone))
        self.db.commit()
        print("Customer added successfully")

    def customer_exists(self, customer_id):
        self.db.cursor.execute(
            "SELECT * FROM customers WHERE customer_id=%s",
            (customer_id,)
        )
        return self.db.cursor.fetchone()

    # -------- BOOKING --------
    def book_room(self, room_id, customer_id, check_in, check_out):

        if not self.customer_exists(customer_id):
            print("Invalid customer ID")
            return

        d1 = datetime.strptime(check_in, "%Y-%m-%d")
        d2 = datetime.strptime(check_out, "%Y-%m-%d")

        days = (d2 - d1).days
        if days <= 0:
            print("Invalid date range")
            return

        # check room
        self.db.cursor.execute(
            "SELECT price, is_available FROM rooms WHERE room_id=%s",
            (room_id,)
        )
        result = self.db.cursor.fetchone()

        if not result:
            print("Invalid room ID")
            return

        price, available = result

        if not available:
            print("Room not available")
            return

        total = price * days

        # insert booking
        self.db.cursor.execute("""
            INSERT INTO bookings (room_id, customer_id, check_in, check_out, total_amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (room_id, customer_id, check_in, check_out, total))

        # update room
        self.db.cursor.execute(
            "UPDATE rooms SET is_available=FALSE WHERE room_id=%s",
            (room_id,)
        )

        self.db.commit()
        print(f"Room booked successfully. Total: {total}")

    def cancel_booking(self, booking_id):
        self.db.cursor.execute(
            "SELECT room_id FROM bookings WHERE booking_id=%s",
            (booking_id,)
        )
        result = self.db.cursor.fetchone()

        if not result:
            print("Invalid booking ID")
            return

        room_id = result[0]

        self.db.cursor.execute(
            "DELETE FROM bookings WHERE booking_id=%s",
            (booking_id,)
        )

        self.db.cursor.execute(
            "UPDATE rooms SET is_available=TRUE WHERE room_id=%s",
            (room_id,)
        )

        self.db.commit()
        print("Booking cancelled")

    def generate_bill(self, booking_id):
        self.db.cursor.execute("""
            SELECT b.booking_id, c.name, r.room_type,
                   b.check_in, b.check_out, b.total_amount
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN rooms r ON b.room_id = r.room_id
            WHERE b.booking_id=%s
        """, (booking_id,))

        bill = self.db.cursor.fetchone()

        if bill:
            print("\n--- BILL DETAILS ---")
            print(f"Booking ID : {bill[0]}")
            print(f"Customer   : {bill[1]}")
            print(f"Room Type  : {bill[2]}")
            print(f"Check-in   : {bill[3]}")
            print(f"Check-out  : {bill[4]}")
            print(f"Total      : {bill[5]}")
        else:
            print("Invalid booking ID")