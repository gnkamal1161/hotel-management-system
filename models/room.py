class Room:
    def __init__(self, db):
        self.db = db

    def add_room(self, room_type, price):
        query = "INSERT INTO rooms (room_type, price, is_available) VALUES (%s, %s, %s)"
        self.db.cursor.execute(query, (room_type, price, True))
        self.db.commit()
        print("Room added successfully")

    def view_available_rooms(self):
        query = "SELECT * FROM rooms WHERE is_available = TRUE"
        self.db.cursor.execute(query)
        rooms = self.db.cursor.fetchall()

        if not rooms:
            print("No rooms available")
        else:
            for room in rooms:
                print(room)