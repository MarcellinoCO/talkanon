import json
from functools import partial

from fastapi import FastAPI

import asyncio
from aio_pika import connect_robust, IncomingMessage

from . import crud, schemas
from .database import SessionLocal

app = FastAPI()


async def consume_message(db, message: IncomingMessage):
    async with message.process():
        print("Hello")
        message_data = json.loads(message.body.decode())
        room_id = message_data["room_id"]
        content = message_data["content"]

        message_data = schemas.MessageBase(content=content)
        created_message = crud.create_message(db, room_id, message_data)
        crud.update_room(db, room_id, created_message.timestamp)


async def main():
    rabbitmq_connection = await connect_robust("amqp://guest:guest@talkanon")

    async with rabbitmq_connection:
        db = SessionLocal()
        channel = await rabbitmq_connection.channel()

        queue_name = "room_messages"
        queue = await channel.declare_queue(queue_name, durable=True)

        await queue.consume(partial(consume_message, db))

        while True:
            await asyncio.sleep(1000)


if __name__ == "__main__":
    asyncio.run(main())
