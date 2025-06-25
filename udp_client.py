import socket
import tkinter as tk
from tkinter import messagebox

# Configuration
PORT = 54321
BUFFER_SIZE = 1024
TIMEOUT = 10  # 5 seconds timeout

# UDP Client UI
class UDPClient:
    def __init__(self, root, server_ip):
        self.server_ip = server_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(TIMEOUT)  # Set socket timeout
        
        self.root = root
        self.root.title("Event Booking System")
        
        tk.Label(root, text=f"Connected to server: {server_ip}").pack()
        
        # Add a refresh button
        self.refresh_button = tk.Button(root, text="Refresh Events List", command=self.refresh_events)
        self.refresh_button.pack()
        
        tk.Label(root, text="Available Events").pack()
        self.events_listbox = tk.Listbox(root, width=50, height=10)
        self.events_listbox.pack()
        
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack()
        self.username_entry.insert(0, "Enter your name")
        
        self.book_button = tk.Button(root, text="Book Event", command=self.book_event)
        self.book_button.pack()
        
        # Status label
        self.status_label = tk.Label(root, text="Status: Ready")
        self.status_label.pack()
        
        # Try to refresh events on startup
        self.root.after(1000, self.refresh_events)
    
    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.root.update()
    
    def send_request(self, request):
        try:
            self.update_status(f"Sending request: {request}")
            self.sock.sendto(request.encode(), (self.server_ip, PORT))
            
            self.update_status("Waiting for response...")
            response, _ = self.sock.recvfrom(BUFFER_SIZE)
            
            response_text = response.decode()
            self.update_status(f"Received: {response_text}")
            return response_text
        except socket.timeout:
            self.update_status("ERROR: Server did not respond (timeout)")
            messagebox.showerror("Connection Error", f"Server at {self.server_ip} did not respond")
            return "ERROR: Timeout"
        except Exception as e:
            self.update_status(f"ERROR: {e}")
            messagebox.showerror("Error", f"Connection error: {e}")
            return f"ERROR: {e}"
    
    def refresh_events(self):
        self.events_listbox.delete(0, tk.END)
        self.update_status("Refreshing events list...")
        response = self.send_request("LIST_EVENTS")
        
        if response.startswith("ERROR"):
            self.events_listbox.insert(tk.END, "Connection error - see status")
            return
            
        if response == "NO_EVENTS":
            self.events_listbox.insert(tk.END, "No events available.")
            self.update_status("No events available in database")
        else:
            events = response.split("|")
            for event in events:
                self.events_listbox.insert(tk.END, event)
            self.update_status(f"Found {len(events)} events")
    
    def book_event(self):
        selected = self.events_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select an event first!")
            return
        
        event_info = self.events_listbox.get(selected[0])
        if event_info == "No events available." or event_info.startswith("Connection error"):
            return
            
        event_id = event_info.split(":")[0]
        username = self.username_entry.get().strip()
        if not username or username == "Enter your name":
            messagebox.showwarning("Warning", "Enter a valid username!")
            return
            
        self.update_status(f"Booking event {event_id} for {username}...")
        response = self.send_request(f"BOOK_EVENT|{event_id}|{username}")
        
        if response == "BOOKING_SUCCESS":
            messagebox.showinfo("Success", "Event booked successfully!")
            self.update_status("Booking successful")
        else:
            messagebox.showerror("Error", f"Booking failed: {response}")
            self.update_status(f"Booking failed: {response}")
        
        self.refresh_events()

if __name__ == "__main__":
    server_ip = input("Enter server IP: ").strip()
    print(f"Attempting to connect to server at {server_ip}:{PORT}")
    
    root = tk.Tk()
    client = UDPClient(root, server_ip)
    root.mainloop()
