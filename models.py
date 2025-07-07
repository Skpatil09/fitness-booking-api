from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class FitnessClass(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    datetime = Column(DateTime)
    instructor = Column(String)
    total_slots = Column(Integer)
    available_slots = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    client_name = Column(String)
    client_email = Column(String)
    booking_time = Column(DateTime)
