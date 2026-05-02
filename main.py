from db.db_connection import DBConnection
from services.hotel_service import HotelService

def main():
    print("Starting Application...")

    db = DBConnection()
    service = HotelService(db)

    while True:
        print("\n--- HOTEL MANAGEMENT SYSTEM ---")
        print("1. Add Room")
        print("2. View Available Rooms")
        print("3. Add Customer")
        print("4. Book Room")
        print("5. Cancel Booking")
        print("6. Generate Bill")
        print("7. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Enter a valid number")
            continue

        if choice == 1:
            rt = input("Room Type: ")
            price = float(input("Price: "))
            service.room.add_room(rt, price)

        elif choice == 2:
            service.room.view_available_rooms()

        elif choice == 3:
            name = input("Name: ")
            phone = input("Phone: ")
            service.cb.add_customer(name, phone)

        elif choice == 4:
            rid = int(input("Room ID: "))
            cid = int(input("Customer ID: "))
            cin = input("Check-in (YYYY-MM-DD): ")
            cout = input("Check-out (YYYY-MM-DD): ")
            service.cb.book_room(rid, cid, cin, cout)

        elif choice == 5:
            bid = int(input("Booking ID: "))
            service.cb.cancel_booking(bid)

        elif choice == 6:
            bid = int(input("Booking ID: "))
            service.cb.generate_bill(bid)

        elif choice == 7:
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()