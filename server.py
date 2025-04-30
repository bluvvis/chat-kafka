from fastapi import FastAPI
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer
import asyncio
import json

app = FastAPI()

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "chat"  # Унифицируем тему

# Модель для входящих сообщений
class Message(BaseModel):
    username: str
    message: str

# Отправка сообщения в Kafka
async def send_to_kafka(message: dict):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()
    try:
        await producer.send_and_wait(KAFKA_TOPIC, json.dumps(message).encode('utf-8'))
        print(f"Отправлено в Kafka: {message}")
    finally:
        await producer.stop()

# Эндпоинт для отправки сообщений
@app.post("/send")
async def send_message(msg: Message):
    message_data = {"user": msg.username, "message": msg.message}
    await send_to_kafka(message_data)
    return {"status": "Message sent"}

# Удаляем потребителя Kafka из server.py, так как он есть в consumer.py
