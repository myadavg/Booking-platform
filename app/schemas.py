from pydantic import BaseModel
from datetime import datetime


class BookingCreate(BaseModel):
    user_name: str
    venue_name: str
    start_time: datetime
    end_time: datetime
