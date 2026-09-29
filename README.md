Campus Event Management API

A RESTful API built with FastAPI and SQLModel for managing campus events and student seat reservations.

Features

- Create and manage campus events
- View available events
- Reserve seats for events
- Check booked and remaining seats
- Prevent overbooking
- Prevent reservations for closed events
- Validate event and reservation data
- Store data using SQLite database
- Use SQLModel Session for database operations

Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

API Operations

Event Management

- Create an event
- Get all events
- Get event details
- Check event availability

Seat Reservation

- Create a reservation
- Check booked seats
- Calculate remaining seats
- Prevent overbooking
- Prevent reservations for closed events

Database

The project uses SQLite as the database and SQLModel for creating models and performing database operations.

How It Works

1. An event is created with a fixed number of seats.
2. Students can reserve seats for an available event.
3. The API checks whether the event exists.
4. The API calculates booked and remaining seats.
5. Reservations are rejected if all seats are already booked.
6. Reservations are also rejected when an event is closed.

Running the Project

uvicorn main:app --reload

After starting the server, open the FastAPI documentation:

/docs

Project Purpose

This project was created to practice FastAPI, database integration, validation, session handling, and real-world reservation logic.
