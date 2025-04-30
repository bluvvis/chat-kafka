import json
import uuid
from fastapi import FastAPI, WebSocket
from aiokafka import AIOKafkaProducer
import asyncio
from pydantic import BaseModel

app = FastAPI()

KAFKA_TOPIC = "chat-messages"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
message_history = []

class Message(BaseModel):
    id: str = None
    user: str
    message: str

producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

@app.on_event("startup")
async def startup_event():
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()

@app.post("/send")
async def send_message(msg: Message):
    if not msg.id:
        msg.id = str(uuid.uuid4())
    message_data = {"id": msg.id, "user": msg.user, "message": msg.message}

    await producer.send_and_wait(
        KAFKA_TOPIC,
        json.dumps(message_data).encode("utf-8")
    )

    message_history.append(message_data)
    if len(message_history) > 100:
        message_history.pop(0)

    return {"status": "Message sent"}

@app.get("/messages")
async def get_messages():
    return {"messages": message_history}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if not message.get("id"):
                message["id"] = str(uuid.uuid4())
            message_history.append(message)
            if len(message_history) > 100:
                message_history.pop(0)
            await websocket.send_text(json.dumps(message))
    except Exception as e:
        print(f"WebSocket error: {e}")
