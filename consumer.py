import asyncio
import json
from aiokafka import AIOKafkaConsumer
import websockets

KAFKA_TOPIC = "chat"
KAFKA_BROKER = "localhost:9092"
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 8001

connected_clients = set()

async def handle_kafka_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='latest',  # Оставляем 'latest', чтобы видеть только новые сообщения
        value_deserializer=lambda m: m.decode('utf-8')
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Получено из Kafka: {message.value}")
            await broadcast(message.value)
    finally:
        await consumer.stop()

async def broadcast(message):
    if connected_clients:
        print(f"Отправляем сообщение {len(connected_clients)} клиентам")
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
    await handle_kafka_messages()

if __name__ == "__main__":
    asyncio.run(main())
