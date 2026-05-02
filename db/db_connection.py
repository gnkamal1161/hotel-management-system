import mysql.connector

class DBConnection:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gnkamal@1161",   # 
                database="hotel_db"
            )
            self.cursor = self.conn.cursor()
            print("Connected to MySQL ")
            self.create_tables()

        except Exception as e:
            print("Database connection failed ")
            print(e)

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INT AUTO_INCREMENT PRIMARY KEY,
            room_type VARCHAR(50),
            price FLOAT,
            is_available BOOLEAN
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(15)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            room_id INT,
            customer_id INT,
            check_in DATE,
            check_out DATE,
            total_amount FLOAT,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        """)

        self.conn.commit()

    def commit(self):
        self.conn.commit()