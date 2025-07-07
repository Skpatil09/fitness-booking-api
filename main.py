from fastapi import FastAPI, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz
from typing import Optional
from database import SessionLocal, engine, Base
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Studio Booking API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper: Convert IST to requested timezone
def convert_timezone(dt, tz: str):
    ist = pytz.timezone('Asia/Kolkata')
    target = pytz.timezone(tz)
    return ist.localize(dt).astimezone(target)

def send_confirmation_email(client_email, client_name, class_name, class_time):
    print(f"[MOCK EMAIL] To: {client_email}")
    print(f"Subject: Booking Confirmed for {class_name}")
    print(f"Hi {client_name}, your spot for {class_name} at {class_time} is confirmed!")

# GET /classes

@app.get("/classes", response_model=list[schemas.FitnessClassOut])
def get_classes(
    tz: str = Query("Asia/Kolkata"),
    name: Optional[str] = None,
    instructor: Optional[str] = None,
    date: Optional[str] = None,  # format: 'YYYY-MM-DD'
    db: Session = Depends(get_db)
):
    query = db.query(models.FitnessClass)
    if name:
        query = query.filter(models.FitnessClass.name.ilike(f"%{name}%"))
    if instructor:
        query = query.filter(models.FitnessClass.instructor.ilike(f"%{instructor}%"))
    if date:
        query = query.filter(models.FitnessClass.datetime.between(f"{date} 00:00:00", f"{date} 23:59:59"))
    classes = query.all()
    for c in classes:
        c.datetime = convert_timezone(c.datetime, tz)
    return classes


# POST /book
@app.post("/book", response_model=schemas.BookingOut)
def book_class(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")
        # Check booking limit: max 3 per week per email
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

    user_bookings_this_week = db.query(models.Booking).filter(
        models.Booking.client_email == booking.client_email,
        models.Booking.booking_time >= start_of_week,
        models.Booking.booking_time <= end_of_week
    ).count()

    if user_bookings_this_week >= 3:
        raise HTTPException(status_code=400, detail="Booking limit of 3 classes per week exceeded.")

    if fitness_class.available_slots < 1:
        raise HTTPException(status_code=400, detail="No slots available")
    # Book
    fitness_class.available_slots -= 1
    db.add(fitness_class)
    db.commit()
    db.refresh(fitness_class)
    new_booking = models.Booking(
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email,
        booking_time=datetime.now()
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    send_confirmation_email(
    client_email=booking.client_email,
    client_name=booking.client_name,
    class_name=fitness_class.name,
    class_time=fitness_class.datetime.strftime("%Y-%m-%d %H:%M")
    )
    return new_booking

# GET /bookings
@app.get("/bookings", response_model=list[schemas.BookingOut])
def get_bookings(email: str, db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).filter(models.Booking.client_email == email).all()
    return bookings

@app.delete("/booking/{booking_id}")
def cancel_booking(
    booking_id: int = Path(..., description="ID of the booking to cancel"),
    db: Session = Depends(get_db)
):
    # Find the booking
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Find the class and increase available slots
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking.class_id).first()
    if fitness_class:
        fitness_class.available_slots += 1
        db.add(fitness_class)

    # Delete the booking
    db.delete(booking)
    db.commit()

    return {"message": f"Booking {booking_id} cancelled successfully."}
