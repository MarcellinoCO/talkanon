from sqlalchemy.orm import Session
from . import models, schemas


def get_rooms(db: Session):
    return db.query(models.Room).all()


def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def create_room(db: Session):
    db_room = models.Room()
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_messages(db: Session, room_id: int):
    return db.query(models.Message).filter(models.Message.room_id == room_id).order_by(models.Message.timestamp).all()


def create_message(db: Session, room_id: int, message: schemas.MessageBase):
    db_message = models.Message(**message.dict(), room_id=room_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
