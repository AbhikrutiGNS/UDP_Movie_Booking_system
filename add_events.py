import sqlite3

# Configuration
DB_NAME = "events.db"

def add_sample_events():
    print("🔧 Adding sample events to database...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if we already have events
    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Add sample events
        sample_events = [
            ("Tech Conference 2025", 50),
            ("Music Festival", 100),
            ("Cooking Workshop", 20),
            ("Programming Bootcamp", 30),
            ("Art Exhibition", 75),
	    ("open mic",2)
        ]
        
        cursor.executemany(
            "INSERT INTO events (name, available_seats) VALUES (?, ?)",
            sample_events
        )
        
        conn.commit()
        print(f"✅ Added {len(sample_events)} sample events!")
    else:
        print(f"ℹ Database already has {count} events, skipping sample data.")
    
    # Display all events
    cursor.execute("SELECT id, name, available_seats FROM events")
    events = cursor.fetchall()
    print("\nCurrent events in database:")
    for event in events:
        print(f"  ID: {event[0]}, Name: {event[1]}, Available Seats: {event[2]}")
    
    conn.close()

if __name__ == "_main_":
    add_sample_events()