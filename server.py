from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer
from fastapi.responses import RedirectResponse
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Константы Kafka ---
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "chat"

# --- Хранилище истории в памяти ---
message_history: list[dict] = []

# --- Схема сообщения ---
class Message(BaseModel):
    user: str
    message: str

# --- Producer для Kafka (один на всё время работы) ---
producer: AIOKafkaProducer | None = None

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    if producer:
        await producer.stop()

# --- Эндпойнт отправки сообщений ---
@app.post("/send")
async def send_message(msg: Message):
    message_data = {"user": msg.user, "message": msg.message}

    # Отправляем в Kafka
    await producer.send_and_wait(
        KAFKA_TOPIC,
        json.dumps(message_data).encode("utf-8")
    )

    # Сохраняем в истории
    message_history.append(message_data)

    if len(message_history) > 100:
        message_history.pop(0)

    return {"status": "Message sent"}

# --- Эндпойнт получения истории сообщений ---
@app.get("/messages")
async def get_messages():
    return {"messages": message_history}

# --- Перенаправление с корневого URL на /web/index.html ---
@app.get("/")
async def redirect_to_index():
    return RedirectResponse(url="/web/index.html")

# --- Подключение директории web для статических файлов ---
app.mount("/web", StaticFiles(directory="web", html=True), name="web")
