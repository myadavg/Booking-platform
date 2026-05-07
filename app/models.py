from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    venue_name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
