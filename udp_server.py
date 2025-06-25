import socket
import threading
import sqlite3

# Configuration
PORT = 54321
BUFFER_SIZE = 1024
DB_NAME = "events.db"

# Initialize Database
def init_db():
    print("🔧 Initializing database...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            available_seats INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            username TEXT,
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

# UDP Server Class
class UDPServer:
    def _init_(self):
        print("🚀 Initializing server...")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"🔄 Created UDP socket on port {PORT}")
            self.sock.bind(("0.0.0.0", PORT))  # Bind to all network interfaces
            print(f"✅ Server started on port {PORT}, listening on all interfaces")
            threading.Thread(target=self.listen_for_requests, daemon=True).start()
        except Exception as e:
            print(f"❌ Error in UDP server: {e}")

    def listen_for_requests(self):
        print("👂 Listening for incoming requests...")
        while True:
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                print(f"📩 Received request: {data.decode()} from {addr}")
                request = data.decode().split("|")
                response = self.handle_request(request)
                self.sock.sendto(response.encode(), addr)
            except Exception as e:
                print(f"⚠ Error in receiving request: {e}")

    def handle_request(self, request):
        if request[0] == "LIST_EVENTS":
            return self.list_events()
        elif request[0] == "BOOK_EVENT":
            if len(request) < 3:
                return "INVALID_REQUEST"
            return self.book_event(request[1], request[2])  # event_id, username
        return "INVALID_REQUEST"

    def list_events(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, available_seats FROM events")
        events = cursor.fetchall()
        conn.close()
        return "|".join([f"{e[0]}: {e[1]} ({e[2]} seats)" for e in events]) if events else "NO_EVENTS"

    def book_event(self, event_id, username):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT available_seats FROM events WHERE id = ?", (event_id,))
        event = cursor.fetchone()
        if event and event[0] > 0:
            cursor.execute("INSERT INTO bookings (event_id, username) VALUES (?, ?)", (event_id, username))
            cursor.execute("UPDATE events SET available_seats = available_seats - 1 WHERE id = ?", (event_id,))
            conn.commit()
            conn.close()
            return "BOOKING_SUCCESS"
        conn.close()
        return "BOOKING_FAILED"

if __name__ == "_main_":
    print("📡 Starting UDP Server...")
    init_db()
    print("⚙ Creating UDP server instance...")
    server = UDPServer()
    print("✅ UDP server should be running now!")
    input("Press Enter to stop the server...")