from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    seat_number = Column(String(20), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    room = relationship("Room", back_populates="seats")
    reservations = relationship("Reservation", back_populates="seat", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Seat(id={self.id}, room_id={self.room_id}, seat_number={self.seat_number})>"
