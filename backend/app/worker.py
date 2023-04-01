import json

from sqlalchemy.orm import Session

import asyncio
import aio_pika

from . import crud
from .database import SessionManager
from .main import app


async def process_message(db: Session, message: aio_pika.IncomingMessage):
    with message.process():
        message_data = json.loads(message.body)
        room_id = message_data["room_id"]
        content = message_data["content"]

        message = crud.create_message(db, room_id, content)
        crud.update_room(db, room_id, message.timestamp)


async def update_queues(db: Session, channel: aio_pika.Channel):
    rooms = await crud.get_rooms_remaining(db, app.state.last_room_id)
    queues = [await channel.declare_queue(f"room_{room.id}_queue") for room in rooms]

    for queue in queues:
        await queue.consume(lambda message: process_message(db, message))

    if queues:
        app.state.last_room_id = max([room.id for room in rooms])


async def main():
    with SessionManager() as db:
        channel = await app.state.rabbitmq_connection.channel()

        app.state.last_room_id = 0
        await update_queues(db, channel)

        while True:
            await asyncio.sleep(1000)
            await update_queues(db, channel)
