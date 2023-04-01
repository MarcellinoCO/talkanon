import json

from dotenv import load_dotenv

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from aio_pika import connect, Message

from . import crud, models, schemas
from .database import SessionLocal, engine

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_rabbitmq_connection():
    return await connect("amqp://guest:guest@talkanon")


@app.on_event("startup")
async def startup_event():
    app.state.rabbitmq_connection = await get_rabbitmq_connection()


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.rabbitmq_connection.close()


@app.get("/")
async def get_rooms():
    return "Welcome to Talkanon!"


@app.get("/rooms", response_model=list[schemas.Room])
async def get_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)


@app.post("/rooms", response_model=schemas.Room)
async def create_rooms(db: Session = Depends(get_db)):
    return crud.create_room(db)


@app.get("/rooms/{room_id}/messages", response_model=list[schemas.Message])
async def get_messages(room_id: int, db: Session = Depends(get_db)):
    return crud.get_messages(db, room_id)


@app.post("/rooms/{room_id}/messages")
async def send_message(room_id: int, content: str, db: Session = Depends(get_db)):
    channel = await app.state.rabbitmq_connection.channel()

    message_data = {"room_id": room_id, "content": content}
    message = Message(json.dumps(message_data).encode())
    await channel.default_exchange.publish(message, routing_key=f"room_{room_id}_queue")
    # queue = await channel.declare_queue(f"room_{room_id}_queue")
    # await queue.publish(Message(json.dumps(message_data).encode()))

    return "ok"
