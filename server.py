import asyncio
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from typing import List

# Инициализация FastAPI приложения
app = FastAPI()

# Конфигурация Kafka Consumer
KAFKA_BROKER = "localhost:9092"  # Адрес вашего брокера Kafka
KAFKA_TOPIC = "chat_topic"  # Тема, которая используется для обмена сообщениями

# Асинхронная функция для обработки сообщений из Kafka
async def consume_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id="chat-consumer-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Получено сообщение: {msg.value.decode()}")
            # Здесь вы можете добавить обработку сообщения (например, сохранять в БД или отправлять на фронт)
    finally:
        await consumer.stop()

# Запуск потребителя Kafka в фоне
@app.on_event("startup")
async def startup_event():
    # Запускаем потребление сообщений Kafka в фоне
    loop = asyncio.get_event_loop()
    loop.create_task(consume_messages())

# Пример маршрута для получения сообщений
@app.get("/messages", response_model=List[str])
async def get_messages():
    # Это просто заглушка, вы можете сюда добавить логику для отображения сообщений
    return ["Пример сообщения 1", "Пример сообщения 2"]

