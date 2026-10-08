from datetime import datetime, date, time

from sqlalchemy import Column, Integer, Date, Time, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    reservation_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(
        Enum("pending", "confirmed", "cancelled", "completed", name="reservation_status"),
        default="confirmed",
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="reservations")
    seat = relationship("Seat", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation(id={self.id}, user_id={self.user_id}, seat_id={self.seat_id})>"
