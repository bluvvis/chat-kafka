from fastapi import FastAPI, Request
from kafka import KafkaProducer, KafkaConsumer
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем фронту обращаться к серверу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'chat',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id="web-client",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

@app.post("/send")
async def send_message(request: Request):
    data = await request.json()
    username = data["username"]
    message = data["message"]
    producer.send('chat', {"username": username, "message": message})
    return {"status": "sent"}

@app.get("/messages")
def get_messages():
    messages = []
    for msg in consumer:
        messages.append(msg.value)
        if len(messages) >= 10:
            break
    return messages

