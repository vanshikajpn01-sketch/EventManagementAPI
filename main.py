from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from database import engine, create_db_and_tables
from models import Event, Reservation
from schemas import EventCreate, EventUpdate, ReservationCreate


app = FastAPI(
    title="College Event Reservation API",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# -------------------------
# EVENT APIs
# -------------------------

# 1. Create Event
@app.post("/events", response_model=Event, status_code=201)
def create_event(event: EventCreate):

    new_event = Event(
        title=event.title,
        venue=event.venue,
        capacity=event.capacity,
        organizer=event.organizer,
        status=event.status
    )

    with Session(engine) as session:
        session.add(new_event)
        session.commit()
        session.refresh(new_event)

        return new_event


# 2. Get All Events
@app.get("/events", response_model=list[Event])
def get_events():

    with Session(engine) as session:
        events = session.exec(select(Event)).all()

        return events


# 3. Get Specific Event
@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        return event


# 4. Update Event
@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, event_data: EventUpdate):

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        event.title = event_data.title
        event.venue = event_data.venue
        event.capacity = event_data.capacity
        event.organizer = event_data.organizer
        event.status = event_data.status

        session.add(event)
        session.commit()
        session.refresh(event)

        return event


# 5. Delete Event
@app.delete("/events/{event_id}")
def delete_event(event_id: int):

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        session.delete(event)
        session.commit()

        return {
            "message": "Event deleted successfully"
        }


# -------------------------
# RESERVATION APIs
# -------------------------

# 6. Create Reservation
@app.post("/events/{event_id}/reserve", response_model=Reservation, status_code=201)
def create_reservation(
    event_id: int,
    reservation_data: ReservationCreate
):

    with Session(engine) as session:

        # Check event exists
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        # Check event status
        if event.status != "Open":
            raise HTTPException(
                status_code=400,
                detail="Event is closed"
            )

        # Count existing reservations
        statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(statement).all()

        booked = len(reservations)

        # Check capacity
        if booked >= event.capacity:
            raise HTTPException(
                status_code=400,
                detail="Event is full"
            )

        # Create reservation
        reservation = Reservation(
            event_id=event_id,
            student_name=reservation_data.student_name,
            roll_number=reservation_data.roll_number,
            email=reservation_data.email
        )

        session.add(reservation)
        session.commit()
        session.refresh(reservation)

        return reservation


# 7. Get Event Reservations
@app.get("/events/{event_id}/reservations")
def get_reservations(event_id: int):

    with Session(engine) as session:

        # Check event exists
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(statement).all()

        return reservations


# 8. Cancel Reservation
@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int):

    with Session(engine) as session:

        reservation = session.get(
            Reservation,
            reservation_id
        )

        if not reservation:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        session.delete(reservation)
        session.commit()

        return {
            "message": "Reservation cancelled successfully"
        }


# 9. Event Availability
@app.get("/events/{event_id}/availability")
def event_availability(event_id: int):

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(statement).all()

        booked = len(reservations)
        remaining = event.capacity - booked

        return {
            "capacity": event.capacity,
            "booked": booked,
            "remaining": remaining
        }