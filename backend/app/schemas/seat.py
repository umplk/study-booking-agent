from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class SeatCreate(BaseModel):
    seat_number: str = Field(..., max_length=20)
    is_available: bool = True


class SeatBatchCreate(BaseModel):
    seats: List[SeatCreate]


class SeatUpdate(BaseModel):
    is_available: Optional[bool] = None
    seat_number: Optional[str] = Field(None, max_length=20)


class SeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    seat_number: str
    is_available: bool
    created_at: datetime
