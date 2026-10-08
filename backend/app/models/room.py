from datetime import datetime, time

from sqlalchemy import Column, Integer, String, Time, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    location = Column(String(200), nullable=True)
    open_time = Column(Time, default=time(8, 0), nullable=False)
    close_time = Column(Time, default=time(22, 0), nullable=False)
    capacity = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    seats = relationship("Seat", back_populates="room", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="room", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name})>"
