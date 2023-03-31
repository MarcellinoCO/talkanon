from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str


class Message(MessageBase):
    id: int
    timestamp: datetime
    room_id: int

    class Config:
        orm_mode = True


class Room(BaseModel):
    id: int
    timestamp: datetime
    items: list[Message] = []

    class Config:
        orm_mode = True
