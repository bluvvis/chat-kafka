from fastapi import FastAPI
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer
import asyncio
import json
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Монтируем папку web для раздачи фронтенда
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "chat"

class Message(BaseModel):
    username: str
    message: str

async def send_to_kafka(message: dict):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()
    try:
        await producer.send_and_wait(KAFKA_TOPIC, json.dumps(message).encode('utf-8'))
        print(f"Отправлено в Kafka: {message}")
    finally:
        await producer.stop()

@app.get("/messages")
async def get_messages():
    return {"messages": []}  # Временное решение

@app.post("/send")
async def send_message(msg: Message):
    message_data = {"user": msg.username, "message": msg.message}
    await send_to_kafka(message_data)
    return {"status": "Message sent"}
