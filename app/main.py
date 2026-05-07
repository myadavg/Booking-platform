from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .schemas import BookingCreate
from .crud import create_booking, get_bookings

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Booking API running - Version 3"}


@app.post("/bookings")
def add_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, booking)


@app.get("/bookings")
def list_bookings(db: Session = Depends(get_db)):
    return get_bookings(db)
