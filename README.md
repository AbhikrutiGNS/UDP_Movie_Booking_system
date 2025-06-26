# UDP based movie booking system

A lightweight and efficient **UDP-based event booking system** built using **Python**, **Tkinter**, and **SQLite3**. This project was developed to demonstrate the use of **socket programming** for real-time booking scenarios.

---

## Tech Stack

- Python  
- Tkinter (GUI)  
- SQLite3 (local database)  
- UDP Socket Programming  

---

##  Features

- Interactive GUI for booking seats  
- Real-time seat availability  
- UDP-based client-server architecture  
- Graceful handling of overbooking or unavailable seats  
- Live update of available seats in the database  

---

## Implementation Overview

1. GUI built using Tkinter for booking interface  
2. UDP sockets for fast and lightweight communication  
3. Server validates requests, manages seat data in SQLite  
4. Client sends booking request and gets success/failure  
5. Real-time updates to the seat count on successful booking  

---

##  Screenshots
###  filling in details
![filling in details](screenshots/udp1.png)
###  Successful Booking  
![Successful Booking](screenshots/udp2.png)

###  Booking Failure (Overbooked)  
![Booking Failure](screenshots/udp4.png)

###  Database Management (Seats Reduced)  
![Seat Reduction](screenshots/udp3.png)
