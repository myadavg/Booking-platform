from .models import Booking


def create_booking(db, booking_data):
    booking = Booking(**booking_data.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_bookings(db):
    return db.query(Booking).all()
