from dotenv import load_dotenv

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from aio_pika import connect

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


@app.get("/", response_model=list[schemas.Room])
async def get_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)
