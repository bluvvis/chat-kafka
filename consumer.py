import asyncio
import json
from kafka import KafkaConsumer
import websockets

KAFKA_TOPIC = "chat"
KAFKA_BROKER = "localhost:9092"
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 8001

connected_clients = set()

async def handle_kafka_messages():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='latest',  # используйте 'earliest', если хотите всю историю
        enable_auto_commit=True,
        value_deserializer=lambda m: m.decode('utf-8')
    )

    print(f"Подключён к Kafka, слушаем топик: {KAFKA_TOPIC}")

    for message in consumer:
        print(f"Получено из Kafka: {message.value}")
        await broadcast(message.value)

async def broadcast(message):
    if connected_clients:
        await asyncio.gather(*(client.send(message) for client in connected_clients))

async def websocket_handler(websocket):
    connected_clients.add(websocket)
    print(f"Клиент подключён: {websocket.remote_address}")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print(f"Клиент отключён: {websocket.remote_address}")

async def main():
    print(f"WebSocket сервер запускается на ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    websocket_server = await websockets.serve(websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT)

    await handle_kafka_messages()  # Запускается после ws-сервера, блокирующая

if __name__ == "__main__":
    asyncio.run(main())
