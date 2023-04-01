import json
import asyncio

from aio_pika import connect_robust, IncomingMessage
from fastapi import FastAPI

from . import crud, schemas
from .database import SessionLocal

app = FastAPI()


async def get_rabbitmq_connection():
    return await connect_robust("amqp://guest:guest@talkanon")


async def on_message(db, message: IncomingMessage):
    async with message.process():
        print("Hello")
        message_data = json.loads(message.body.decode())
        room_id = message_data["room_id"]
        content = message_data["content"]

        message_data = schemas.MessageBase(content=content)
        created_message = crud.create_message(db, room_id, message_data)
        crud.update_room(db, room_id, created_message.timestamp)


async def main():
    rabbitmq_connection = await get_rabbitmq_connection()

    async with rabbitmq_connection:
        db = SessionLocal()
        channel = await rabbitmq_connection.channel()

        queue_name = "room_messages"
        queue = await channel.declare_queue(queue_name, durable=True)

        await queue.consume(lambda message: on_message(db, message))

        while True:
            await asyncio.sleep(1000)


if __name__ == "__main__":
    asyncio.run(main())
