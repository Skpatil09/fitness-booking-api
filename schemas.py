from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class FitnessClassOut(BaseModel):
    id: int
    name: str
    datetime: datetime
    instructor: str
    available_slots: int

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    class_id: int
    client_name: str = Field(..., min_length=1, description="Client name must not be empty")
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    booking_time: datetime

    class Config:
        from_attributes = True
