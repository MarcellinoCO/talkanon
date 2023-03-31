from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="messages")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    messages = relationship("Message", back_populates="room")
