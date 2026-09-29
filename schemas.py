from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel


class EventCreate(SQLModel):
    title: str
    venue: str
    capacity: int
    organizer: str
    status: str = "Open"

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value):
        if value <= 0:
            raise ValueError("Capacity must be greater than 0")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value not in ["Open", "Closed"]:
            raise ValueError("Status must be Open or Closed")
        return value


class EventUpdate(SQLModel):
    title: str
    venue: str
    capacity: int
    organizer: str
    status: str

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value):
        if value <= 0:
            raise ValueError("Capacity must be greater than 0")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value not in ["Open", "Closed"]:
            raise ValueError("Status must be Open or Closed")
        return value


class ReservationCreate(SQLModel):
    student_name: str
    roll_number: str
    email: EmailStr

    @field_validator("student_name")
    @classmethod
    def validate_student_name(cls, value):
        if not value.strip():
            raise ValueError("Student name cannot be empty")
        return value